"""
Admin tools endpoints - untuk maintenance dan fix data
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

from app.database import get_db
from app.dependencies import require_role
from app.models.user import User, UserRole
from app.utils.password import hash_password
from app.utils.response import base_response

router = APIRouter(
    prefix="/admin-tools",
    tags=["Admin Tools"],
    dependencies=[Depends(require_role(UserRole.superadmin))]  # Only superadmin
)


@router.post("/fix-all-passwords")
async def fix_all_user_passwords(db: Session = Depends(get_db)):
    """
    Fix password semua user yang ter-upload dengan format salah.
    
    Password lama: hanya DDMMYYYY (contoh: 25072004)
    Password baru: namadepan + DDMMYYYY (contoh: nurdayani25072004)
    
    ⚠️ HANYA SUPERADMIN yang bisa akses endpoint ini!
    """
    try:
        # Get all users yang punya birth_date
        users = db.query(User).filter(
            User.birth_date.isnot(None)
        ).all()
        
        if len(users) == 0:
            return base_response(
                message="Tidak ada user dengan birth_date yang perlu di-fix",
                payload={"updated_count": 0, "users": []}
            )
        
        updated_users = []
        updated_count = 0
        
        # Reset passwords
        for user in users:
            try:
                # Generate password baru: namadepan + DDMMYYYY
                first_name = user.full_name.split()[0].lower()
                date_str = user.birth_date.strftime("%d%m%Y")
                new_password = f"{first_name}{date_str}"
                
                # Hash dan update
                user.password_hash = hash_password(new_password)
                updated_count += 1
                
                # Track untuk response
                updated_users.append({
                    "id": str(user.id),
                    "full_name": user.full_name,
                    "phone_number": user.phone_number,
                    "email": user.email,
                    "new_password": new_password,
                    "role": user.role.value
                })
                
            except Exception as e:
                # Skip user yang error
                print(f"Error untuk {user.full_name}: {str(e)}")
                continue
        
        # Commit semua changes
        db.commit()
        
        return base_response(
            message=f"Berhasil reset {updated_count} user passwords!",
            payload={
                "updated_count": updated_count,
                "total_users": len(users),
                "users": updated_users
            }
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fixing passwords: {str(e)}"
        )


@router.get("/user-credentials")
async def get_all_user_credentials(db: Session = Depends(get_db)):
    """
    Get list semua user dengan password mereka (generated).
    
    ⚠️ HANYA SUPERADMIN yang bisa akses endpoint ini!
    Gunakan untuk dokumentasi atau sharing ke user.
    """
    try:
        # Get all users yang punya birth_date
        users = db.query(User).filter(
            User.birth_date.isnot(None),
            User.is_active == True
        ).all()
        
        credentials = []
        for user in users:
            first_name = user.full_name.split()[0].lower()
            date_str = user.birth_date.strftime("%d%m%Y")
            password = f"{first_name}{date_str}"
            
            credentials.append({
                "full_name": user.full_name,
                "phone_number": user.phone_number,
                "email": user.email,
                "password": password,
                "role": user.role.value,
                "kategori": user.kategori_pengguna.value
            })
        
        return base_response(
            message=f"Ditemukan {len(credentials)} user credentials",
            payload={"credentials": credentials}
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting credentials: {str(e)}"
        )
