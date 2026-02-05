from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from uuid import UUID
import logging

from app.database import get_db
from app.models.user import User, UserRole
from app.models.vehicle import Vehicle, UnitKategori
from app.schemas.vehicle import VehicleCreate, VehicleUpdate, VehicleResponse
from app.dependencies import get_current_user, require_role
from app.services.p2h_service import p2h_service
from app.utils.response import base_response
from app.repositories.vehicle_repository import vehicle_repository 

logger = logging.getLogger(__name__)

router = APIRouter()

# --- ENDPOINT PUBLIK (TANPA LOGIN) ---

@router.get("/lambung/{no_lambung}")
async def get_vehicle_by_lambung(
    no_lambung: str,
    db: Session = Depends(get_db)
):
    """
    Mencari kendaraan berdasarkan nomor lambung ATAU nomor polisi secara publik.
    Digunakan oleh driver untuk validasi unit sebelum mengisi form P2H.
    Mendukung format fleksibel: P309, P.309, p 309, P,309 semua akan ditemukan.
    
    Untuk unit TRAVEL (tanpa nomor lambung), bisa search menggunakan nomor polisi.
    """
    vehicle = None
    
    # Coba cari berdasarkan nomor lambung dulu (untuk unit IMM)
    vehicle = vehicle_repository.get_by_hull_number(db, no_lambung)
    
    # Jika tidak ditemukan, coba cari berdasarkan nomor polisi (untuk unit TRAVEL)
    if not vehicle:
        # Normalize plat nomor (uppercase dan tanpa spasi)
        normalized_plat = no_lambung.upper().replace(" ", "").replace("-", "")
        
        vehicle = db.query(Vehicle).filter(
            Vehicle.is_active == True
        ).filter(
            Vehicle.plat_nomor.ilike(f"%{no_lambung}%")
        ).first()
        
        # Jika masih tidak ditemukan dengan LIKE, coba exact match dengan normalisasi
        if not vehicle:
            all_vehicles = db.query(Vehicle).filter(Vehicle.is_active == True).all()
            for v in all_vehicles:
                if v.plat_nomor:
                    v_normalized = v.plat_nomor.upper().replace(" ", "").replace("-", "")
                    if v_normalized == normalized_plat:
                        vehicle = v
                        break
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kendaraan dengan nomor lambung/polisi '{no_lambung}' tidak ditemukan"
        )
    
    # Mendapatkan status P2H hari ini (Shift, ketersediaan, dll)
    p2h_status = p2h_service.get_vehicle_p2h_status(db, vehicle.id)
    
    # Debug log untuk troubleshooting
    logger.info(f"🔍 [P2H Status Debug] Vehicle: {no_lambung}")
    logger.info(f"🔍 [P2H Status Debug] color_code: {p2h_status['color_code']}")
    logger.info(f"🔍 [P2H Status Debug] shifts_completed: {p2h_status['shifts_completed']}")
    logger.info(f"🔍 [P2H Status Debug] status_p2h: {p2h_status['status_p2h']}")
    
    # Cek apakah masih bisa submit P2H
    current_shift = p2h_status["current_shift"]
    can_submit, submit_message = p2h_service.can_submit_p2h(db, vehicle, current_shift)
    
    # Cek apakah sudah P2H hari ini (minimal 1 shift sudah selesai)
    # Green atau Yellow berarti ada shift yang sudah dikerjakan
    p2h_completed_today = p2h_status["color_code"] in ["green", "yellow"]
    
    logger.info(f"🔍 [P2H Status Debug] p2h_completed_today: {p2h_completed_today}")
    
    # Gabungkan data kendaraan dan status P2H dalam satu payload
    result = {
        "vehicle": VehicleResponse.model_validate(vehicle).model_dump(mode='json'),
        "can_submit_p2h": can_submit,
        "p2h_completed_today": p2h_completed_today,
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

# Endpoints khusus harus didefinisikan SEBELUM endpoint generic untuk menghindari konflik routing

@router.post("/travel/restore-or-create")
async def restore_or_create_travel_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Untuk TRAVEL vehicles: Check apakah plat_nomor sudah exist (deleted atau tidak).
    - Jika exist dan deleted (is_active=False): RESTORE data lama dengan update field baru
    - Jika exist dan active: Return error
    - Jika tidak exist: CREATE vehicle baru
    
    Ini penting karena plat_nomor adalah unique key untuk TRAVEL.
    Soft delete bukan hard delete, jadi data masih ada di database.
    """
    from datetime import datetime
    
    if vehicle_data.kategori_unit != UnitKategori.TRAVEL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Endpoint ini hanya untuk kategori TRAVEL"
        )
    
    plat_nomor = vehicle_data.plat_nomor
    
    # Check apakah plat_nomor sudah ada di database
    existing_vehicle = db.query(Vehicle).filter(
        Vehicle.plat_nomor == plat_nomor
    ).first()
    
    if existing_vehicle:
        if existing_vehicle.is_active:
            # Sudah active - error
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Nomor polisi {plat_nomor} sudah terdaftar dan masih aktif"
            )
        else:
            # Soft deleted - RESTORE dan update data
            logger.info(f"🔄 Restoring deleted vehicle with plat_nomor: {plat_nomor}")
            
            # Update semua field dari vehicle_data kecuali id, created_at
            for field, value in vehicle_data.model_dump(exclude_unset=True).items():
                if field not in ['id', 'created_at']:
                    setattr(existing_vehicle, field, value)
            
            # Restore dengan set is_active = True
            existing_vehicle.is_active = True
            existing_vehicle.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(existing_vehicle)
            
            logger.info(f"✅ Vehicle restored successfully: {plat_nomor}")
            
            return base_response(
                message="Kendaraan berhasil dipulihkan (Restore dari data terhapus)",
                payload=VehicleResponse.model_validate(existing_vehicle).model_dump(mode='json'),
                status_code=status.HTTP_200_OK
            )
    
    # Tidak ada existing vehicle - CREATE baru
    vehicle = Vehicle(**vehicle_data.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    
    logger.info(f"✅ New vehicle created: {plat_nomor}")
    
    return base_response(
        message="Kendaraan baru berhasil ditambahkan",
        payload=VehicleResponse.model_validate(vehicle).model_dump(mode='json'),
        status_code=status.HTTP_201_CREATED
    )


@router.post("/imm/restore-or-create")
async def restore_or_create_imm_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Untuk IMM (Unit PT) vehicles: Check apakah no_lambung sudah exist (deleted atau tidak).
    - Jika exist dan deleted (is_active=False): RESTORE data lama dengan update field baru
    - Jika exist dan active: Return error
    - Jika tidak exist: CREATE vehicle baru
    
    Ini penting karena no_lambung adalah unique key untuk IMM.
    Soft delete bukan hard delete, jadi data masih ada di database.
    """
    from datetime import datetime
    
    if vehicle_data.kategori_unit != UnitKategori.IMM:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Endpoint ini hanya untuk kategori IMM"
        )
    
    no_lambung = vehicle_data.no_lambung
    
    # Check apakah no_lambung sudah ada di database
    existing_vehicle = db.query(Vehicle).filter(
        Vehicle.no_lambung == no_lambung
    ).first()
    
    if existing_vehicle:
        if existing_vehicle.is_active:
            # Sudah active - error
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Nomor lambung {no_lambung} sudah terdaftar dan masih aktif"
            )
        else:
            # Soft deleted - RESTORE dan update data
            logger.info(f"🔄 Restoring deleted vehicle with no_lambung: {no_lambung}")
            
            # Update semua field dari vehicle_data kecuali id, created_at
            for field, value in vehicle_data.model_dump(exclude_unset=True).items():
                if field not in ['id', 'created_at']:
                    setattr(existing_vehicle, field, value)
            
            # Restore dengan set is_active = True
            existing_vehicle.is_active = True
            existing_vehicle.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(existing_vehicle)
            
            logger.info(f"✅ Vehicle restored successfully: {no_lambung}")
            
            return base_response(
                message="Kendaraan berhasil dipulihkan (Restore dari data terhapus)",
                payload=VehicleResponse.model_validate(existing_vehicle).model_dump(mode='json'),
                status_code=status.HTTP_200_OK
            )
    
    # Tidak ada existing vehicle - CREATE baru
    vehicle = Vehicle(**vehicle_data.model_dump())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    
    logger.info(f"✅ New vehicle created: {no_lambung}")
    
    return base_response(
        message="Kendaraan baru berhasil ditambahkan",
        payload=VehicleResponse.model_validate(vehicle).model_dump(mode='json'),
        status_code=status.HTTP_201_CREATED
    )


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Menambah kendaraan baru (Superadmin dan Admin).
    """
    # Check duplicate no_lambung only if provided (not for TRAVEL category)
    if vehicle_data.no_lambung:
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
    limit: int = Query(100, ge=1, le=500),
    search: Optional[str] = Query(None, description="Cari berdasarkan nomor lambung, plat, atau merk"),
    vehicle_type: Optional[str] = Query(None, description="Filter tipe kendaraan"),
    is_active: Optional[bool] = Query(None, description="Filter status aktif"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Mendapatkan semua daftar kendaraan (Wajib Login).
    Search mendukung format fleksibel untuk nomor lambung: P309, P.309, p 309, dll.
    """
    try:
        # Default filter untuk is_active
        is_active_filter = True if is_active is None else is_active
        
        # Query langsung dengan eager loading untuk relasi
        query = db.query(Vehicle).options(
            joinedload(Vehicle.user),
            joinedload(Vehicle.company)
        ).filter(Vehicle.is_active == is_active_filter)
        
        # Filter by vehicle_type if provided
        if vehicle_type:
            query = query.filter(Vehicle.vehicle_type == vehicle_type)
        
        # Simple search tanpa normalisasi yang berat
        if search and search.strip():
            search_term = f"%{search.strip().upper()}%"
            query = query.filter(
                (Vehicle.no_lambung.ilike(search_term)) |
                (Vehicle.plat_nomor.ilike(search_term)) |
                (Vehicle.merk.ilike(search_term))
            )
        
        # Apply pagination di database level
        vehicles = query.offset(skip).limit(limit).all()
        
        payload = [VehicleResponse.model_validate(v).model_dump(mode='json') for v in vehicles]
        
        return base_response(
            message="Daftar kendaraan berhasil diambil",
            payload=payload
        )
    except Exception as e:
        logger.error(f"Error fetching vehicles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Gagal mengambil data kendaraan: {str(e)}"
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

@router.post("/bulk-delete")
async def bulk_delete_vehicles(
    request: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.superadmin, UserRole.admin))
):
    """
    Bulk soft delete vehicles for better performance.
    
    Request body:
    {
        "ids": ["uuid1", "uuid2", "uuid3", ...]
    }
    """
    from datetime import datetime
    
    ids = request.get('ids', [])
    
    if not ids or not isinstance(ids, list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="IDs array required"
        )
    
    # Convert string IDs to UUID
    try:
        vehicle_ids = [UUID(str(id)) for id in ids]
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid UUID format: {str(e)}"
        )
    
    # Bulk update using SQL for better performance
    # Vehicle model uses is_active for soft delete (no is_deleted field)
    deleted_count = db.query(Vehicle).filter(
        Vehicle.id.in_(vehicle_ids),
        Vehicle.is_active == True
    ).update(
        {
            'is_active': False,
            'updated_at': datetime.utcnow()
        },
        synchronize_session=False
    )
    
    db.commit()
    
    return base_response(
        message=f"{deleted_count} vehicles successfully deleted",
        payload={
            "deleted_count": deleted_count,
            "requested_count": len(ids)
        }
    )
