"""
Vehicle Types Router - CRUD operations for vehicle types

Currently uses in-memory storage with enum values as seed data.
This can be upgraded to a proper database table in the future.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User, UserRole
from app.models.vehicle import VehicleType
from app.dependencies import get_current_user, require_role
from app.utils.response import base_response

router = APIRouter()


# --- SCHEMAS ---
class VehicleTypeBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True


class VehicleTypeCreate(VehicleTypeBase):
    pass


class VehicleTypeUpdate(VehicleTypeBase):
    pass


class VehicleTypeResponse(VehicleTypeBase):
    id: str
    
    class Config:
        from_attributes = True


# --- IN-MEMORY STORAGE (seeded from enum) ---
# This simulates a database table using the enum values as initial data
_vehicle_types_store = {}


def _init_vehicle_types():
    """Initialize vehicle types from enum if empty"""
    global _vehicle_types_store
    if not _vehicle_types_store:
        for vt in VehicleType:
            type_id = str(uuid4())
            _vehicle_types_store[type_id] = {
                "id": type_id,
                "name": vt.value,
                "description": f"Kendaraan tipe {vt.value}",
                "is_active": True
            }


# Initialize on module load
_init_vehicle_types()


# --- ENDPOINTS ---

@router.get("/active")
async def get_active_vehicle_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all active vehicle types.
    Used for dropdown/selection in forms.
    """
    active_types = [
        vt for vt in _vehicle_types_store.values() 
        if vt["is_active"]
    ]
    
    return base_response(
        message="Tipe kendaraan aktif berhasil diambil",
        payload=active_types
    )


@router.get("")
async def get_vehicle_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = Query(None, description="Search by name"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Get all vehicle types with pagination and filters.
    Admin/Superadmin only.
    """
    types_list = list(_vehicle_types_store.values())
    
    # Apply filters
    if search:
        search_lower = search.lower()
        types_list = [vt for vt in types_list if search_lower in vt["name"].lower()]
    
    if is_active is not None:
        types_list = [vt for vt in types_list if vt["is_active"] == is_active]
    
    # Get total count before pagination
    total = len(types_list)
    
    # Apply pagination
    paginated = types_list[skip:skip + limit]
    
    return base_response(
        message="Daftar tipe kendaraan berhasil diambil",
        payload={
            "items": paginated,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    )


@router.get("/{type_id}")
async def get_vehicle_type(
    type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get vehicle type by ID.
    """
    vehicle_type = _vehicle_types_store.get(type_id)
    if not vehicle_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipe kendaraan tidak ditemukan"
        )
    
    return base_response(
        message="Tipe kendaraan ditemukan",
        payload=vehicle_type
    )


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_vehicle_type(
    data: VehicleTypeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Create new vehicle type.
    Admin/Superadmin only.
    """
    # Check for duplicate name
    for vt in _vehicle_types_store.values():
        if vt["name"].lower() == data.name.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tipe kendaraan dengan nama '{data.name}' sudah ada"
            )
    
    # Create new vehicle type
    type_id = str(uuid4())
    new_type = {
        "id": type_id,
        "name": data.name,
        "description": data.description,
        "is_active": data.is_active
    }
    
    _vehicle_types_store[type_id] = new_type
    
    return base_response(
        message="Tipe kendaraan berhasil ditambahkan",
        payload=new_type,
        status_code=status.HTTP_201_CREATED
    )


@router.put("/{type_id}")
async def update_vehicle_type(
    type_id: str,
    data: VehicleTypeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Update vehicle type.
    Admin/Superadmin only.
    """
    if type_id not in _vehicle_types_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipe kendaraan tidak ditemukan"
        )
    
    # Check for duplicate name (excluding current)
    for vt_id, vt in _vehicle_types_store.items():
        if vt_id != type_id and vt["name"].lower() == data.name.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Tipe kendaraan dengan nama '{data.name}' sudah ada"
            )
    
    # Update
    _vehicle_types_store[type_id].update({
        "name": data.name,
        "description": data.description,
        "is_active": data.is_active
    })
    
    return base_response(
        message="Tipe kendaraan berhasil diupdate",
        payload=_vehicle_types_store[type_id]
    )


@router.delete("/{type_id}")
async def delete_vehicle_type(
    type_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Delete vehicle type (soft delete - sets is_active to False).
    Admin/Superadmin only.
    """
    if type_id not in _vehicle_types_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tipe kendaraan tidak ditemukan"
        )
    
    # Soft delete
    _vehicle_types_store[type_id]["is_active"] = False
    
    return base_response(
        message="Tipe kendaraan berhasil dihapus",
        payload={"id": type_id}
    )
