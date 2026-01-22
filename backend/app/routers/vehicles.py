from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional
from uuid import UUID
import re

from app.database import get_db
from app.models.user import User, UserRole
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.dependencies import get_current_user, require_role
from app.services.p2h_service import p2h_service
from app.utils.response import base_response 

router = APIRouter()


# --- HELPER FUNCTIONS ---

def normalize_lambung_search(search_input: str) -> str:
    """
    Normalisasi input pencarian nomor lambung.
    Menghapus karakter non-alphanumeric dan mengubah ke uppercase.
    
    Contoh:
    - 'P.309' -> 'P309'
    - '309' -> '309'
    - 'p309' -> 'P309'
    - 'P-309' -> 'P309'
    """
    # Hapus semua karakter non-alphanumeric (titik, dash, spasi, dll)
    normalized = re.sub(r'[^a-zA-Z0-9]', '', search_input)
    return normalized.upper()


def create_lambung_search_pattern(normalized_input: str) -> str:
    """
    Membuat pattern SQL LIKE untuk pencarian fleksibel.
    
    Contoh:
    - '309' -> '%309%' (cari angka saja di mana saja)
    - 'P309' -> '%P%309%' atau '%P.309%' atau '%P-309%'
    """
    # Jika input hanya angka, cari pattern angka tersebut
    if normalized_input.isdigit():
        return f'%{normalized_input}%'
    
    # Jika ada huruf dan angka, pisahkan untuk pencarian fleksibel
    # Contoh: P309 -> cari P diikuti 309 dengan karakter apapun di antaranya
    letters = re.sub(r'[0-9]', '', normalized_input)  # Ambil huruf saja
    numbers = re.sub(r'[^0-9]', '', normalized_input)  # Ambil angka saja
    
    if letters and numbers:
        # Pattern: huruf + karakter apapun + angka
        return f'%{letters}%{numbers}%'
    
    return f'%{normalized_input}%'


# --- ENDPOINT PUBLIK (TANPA LOGIN) ---

@router.get("/lambung/{no_lambung}")
async def get_vehicle_by_lambung(
    no_lambung: str,
    db: Session = Depends(get_db)
):
    """
    Mencari kendaraan berdasarkan nomor lambung secara publik.
    Digunakan oleh driver untuk validasi unit sebelum mengisi form P2H.
    
    Pencarian dinamis mendukung format:
    - 'P.309' (format lengkap)
    - '309' (angka saja)
    - 'p309', 'P309' (tanpa titik/dash)
    - 'P-309' (dengan dash)
    """
    # Normalisasi input pencarian
    normalized_search = normalize_lambung_search(no_lambung)
    search_pattern = create_lambung_search_pattern(normalized_search)
    
    # Strategi 1: Exact match (paling cepat)
    vehicle = db.query(Vehicle).filter(Vehicle.no_lambung == no_lambung).first()
    
    # Strategi 2: Case-insensitive exact match
    if not vehicle:
        vehicle = db.query(Vehicle).filter(
            func.upper(Vehicle.no_lambung) == no_lambung.upper()
        ).first()
    
    # Strategi 3: ILIKE pattern matching (untuk format berbeda)
    if not vehicle:
        vehicle = db.query(Vehicle).filter(
            Vehicle.no_lambung.ilike(search_pattern)
        ).first()
    
    # Strategi 4: Normalisasi di Python (untuk kompatibilitas database)
    # Ambil kandidat dengan pattern dasar, lalu filter di Python
    if not vehicle:
        # Ambil angka dari input untuk pencarian
        numbers_only = re.sub(r'[^0-9]', '', normalized_search)
        if numbers_only:
            candidates = db.query(Vehicle).filter(
                Vehicle.no_lambung.ilike(f'%{numbers_only}%')
            ).limit(20).all()
            
            # Filter di Python dengan normalisasi
            for candidate in candidates:
                candidate_normalized = normalize_lambung_search(candidate.no_lambung)
                if candidate_normalized == normalized_search:
                    vehicle = candidate
                    break
                # Cek juga jika angka sama (untuk kasus input hanya angka)
                if numbers_only == re.sub(r'[^0-9]', '', candidate_normalized):
                    vehicle = candidate
                    break
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kendaraan dengan nomor lambung {no_lambung} tidak ditemukan"
        )
    
    # Mendapatkan status P2H hari ini (Shift, ketersediaan, dll)
    p2h_status = p2h_service.get_vehicle_p2h_status(db, vehicle.id)
    
    # Cek apakah masih bisa submit P2H
    current_shift = p2h_status["current_shift"]
    can_submit, submit_message = p2h_service.can_submit_p2h(db, vehicle, current_shift)
    
    # Gabungkan data kendaraan dan status P2H dalam satu payload
    result = {
        "vehicle": VehicleResponse.model_validate(vehicle).model_dump(mode='json'),
        "can_submit_p2h": can_submit,
        "p2h_completed_today": p2h_status["color_code"] == "green",
        "current_shift": current_shift,
        "shifts_completed": p2h_status["shifts_completed"],
        "status_p2h": p2h_status["status_p2h"],
        "color_code": p2h_status["color_code"],
        "message": submit_message
    }
    
    return base_response(
        message="Data unit dan status P2H berhasil ditemukan",
        payload=result
    )


# --- ENDPOINT TERPROTEKSI (WAJIB LOGIN) ---

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Menambah kendaraan baru (Superadmin dan Admin).
    """
    existing = db.query(Vehicle).filter(
        Vehicle.no_lambung == vehicle_data.no_lambung,
        Vehicle.is_active == True
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nomor lambung {vehicle_data.no_lambung} sudah terdaftar"
        )
    
    vehicle = Vehicle(**vehicle_data.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    
    return base_response(
        message="Data kendaraan berhasil ditambahkan",
        payload=VehicleResponse.model_validate(vehicle).model_dump(mode='json'),
        status_code=status.HTTP_201_CREATED
    )


@router.get("")
async def get_vehicles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = Query(None, description="Cari berdasarkan nomor lambung, plat, atau merk"),
    vehicle_type: Optional[str] = Query(None, description="Filter tipe kendaraan"),
    is_active: Optional[bool] = Query(None, description="Filter status aktif"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mendapatkan semua daftar kendaraan (Wajib Login).
    """
    query = db.query(Vehicle).options(
        joinedload(Vehicle.user),
        joinedload(Vehicle.company)
    )
    
    # Default: hanya ambil data aktif, kecuali is_active diset eksplisit
    if is_active is None:
        query = query.filter(Vehicle.is_active == True)
    else:
        query = query.filter(Vehicle.is_active == is_active)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Vehicle.no_lambung.ilike(search_term)) |
            (Vehicle.plat_nomor.ilike(search_term)) |
            (Vehicle.merk.ilike(search_term))
        )
    
    if vehicle_type:
        query = query.filter(Vehicle.vehicle_type == vehicle_type)
    
    vehicles = query.offset(skip).limit(limit).all()
    payload = [VehicleResponse.model_validate(v).model_dump(mode='json') for v in vehicles]
    
    return base_response(
        message="Daftar kendaraan berhasil diambil",
        payload=payload
    )


@router.get("/{vehicle_id}")
async def get_vehicle(
    vehicle_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mendapatkan detail kendaraan berdasarkan ID (Wajib Login).
    """
    vehicle = db.query(Vehicle).options(
        joinedload(Vehicle.user),
        joinedload(Vehicle.company)
    ).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kendaraan tidak ditemukan"
        )
    
    return base_response(
        message="Data kendaraan ditemukan",
        payload=VehicleResponse.model_validate(vehicle).model_dump(mode='json')
    )


@router.put("/{vehicle_id}")
async def update_vehicle(
    vehicle_id: UUID,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Memperbarui data kendaraan (Superadmin dan Admin).
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kendaraan tidak ditemukan"
        )
    
    if vehicle_data.no_lambung and vehicle_data.no_lambung != vehicle.no_lambung:
        existing = db.query(Vehicle).filter(
            Vehicle.no_lambung == vehicle_data.no_lambung,
            Vehicle.id != vehicle_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Nomor lambung {vehicle_data.no_lambung} sudah terdaftar"
            )
    
    for field, value in vehicle_data.model_dump(exclude_unset=True).items():
        setattr(vehicle, field, value)
    
    db.commit()
    db.refresh(vehicle)
    
    return base_response(
        message="Data kendaraan berhasil diperbarui",
        payload=VehicleResponse.model_validate(vehicle).model_dump(mode='json')
    )


@router.delete("/{vehicle_id}")
async def delete_vehicle(
    vehicle_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Menonaktifkan kendaraan/Soft Delete (Superadmin dan Admin).
    """
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kendaraan tidak ditemukan"
        )
    
    vehicle.is_active = False
    db.commit()
    
    return base_response(
        message="Kendaraan berhasil dinonaktifkan",
        payload={"vehicle_id": str(vehicle_id)}
    )