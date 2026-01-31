from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from app.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.auth_service import auth_service
from app.dependencies import get_current_user, require_role
from app.utils.response import base_response 

router = APIRouter()

@router.get("/me")
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get current logged-in user profile.
    Accessible by all authenticated users.
    """
    return base_response(
        message="Data profil berhasil diambil",
        payload=UserResponse.model_validate(current_user).model_dump(mode='json')
    )

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Menambah Karyawan/User Baru (Superadmin dan Admin).
    Password akan otomatis dibuat: namadepan + DDMMYYYY jika dikosongkan.
    
    Business Rules:
    - Admin dan Superadmin memiliki akses setara
    - Keduanya dapat membuat user dengan role: user, admin, atau superadmin
    """
    try:
        user = auth_service.create_user(db, user_data)
        return base_response(
            message="User berhasil didaftarkan ke sistem",
            payload=UserResponse.model_validate(user).model_dump(mode='json'),
            status_code=status.HTTP_201_CREATED
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Log unexpected errors for debugging
        import logging
        logging.error(f"Error creating user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal membuat user: {str(e)}"
        )

@router.get("")
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(2000, ge=1, le=2000),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Melihat Daftar Semua User (Superadmin dan Admin).
    """
    users = auth_service.get_all_users(db, skip=skip, limit=limit)
    # Data dikonversi ke UserResponse agar password_hash tidak ikut terkirim
    payload = [UserResponse.model_validate(u).model_dump(mode='json') for u in users]
    
    return base_response(
        message="Daftar user berhasil diambil",
        payload=payload
    )

@router.get("/{user_id}")
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Melihat Detail User berdasarkan ID.
    """
    user = auth_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan"
        )
    
    return base_response(
        message="Data user ditemukan",
        payload=UserResponse.model_validate(user).model_dump(mode='json')
    )

@router.put("/{user_id}")
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Memperbarui Data User (Superadmin dan Admin).
    """
    try:
        user = auth_service.update_user(db, user_id, user_data)
        return base_response(
            message="Data user berhasil diperbarui",
            payload=UserResponse.model_validate(user).model_dump(mode='json')
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Menonaktifkan User (Soft Delete, Superadmin dan Admin).
    """
    success = auth_service.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan"
        )
    
    return base_response(
        message="User berhasil dinonaktifkan",
        payload={"user_id": str(user_id)}
    )

@router.post("/bulk-delete")
async def bulk_delete_users(
    request: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Bulk soft delete users for better performance.
    
    Request body:
    {
        "ids": ["uuid1", "uuid2", "uuid3", ...]
    }
    """
    ids = request.get('ids', [])
    
    if not ids or not isinstance(ids, list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IDs array required"
        )
    
    # Convert string IDs to UUID
    try:
        user_ids = [UUID(str(id)) for id in ids]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid UUID format: {str(e)}"
        )
    
    # Bulk update using SQL for better performance
    # User model uses is_active for soft delete (no is_deleted field)
    deleted_count = db.query(User).filter(
        User.id.in_(user_ids),
        User.is_active == True
    ).update(
        {
            'is_active': False,
            'updated_at': datetime.utcnow()
        },
        synchronize_session=False
    )
    
    db.commit()
    
    return base_response(
        message=f"{deleted_count} users successfully deleted",
        payload={
            "deleted_count": deleted_count,
            "requested_count": len(ids)
        }
    )
