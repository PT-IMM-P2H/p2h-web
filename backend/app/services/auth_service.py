from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID
from fastapi import HTTPException, status  # Import wajib untuk handle error API

from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.user import UserCreate, UserUpdate
from app.utils.password import hash_password, verify_password, generate_username


class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user with auto-generated password.
        
        Password format: namadepan + DDMMYYYY (contoh: yunnifa12062003)
        Jika birth_date kosong dan password tidak disediakan, akan error.
        """
        # Check if phone number already exists
        existing_user = db.query(User).filter(
            User.phone_number == user_data.phone_number
        ).first()
        
        if existing_user:
            # GANTI ValueError -> HTTPException 400
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Nomor telepon {user_data.phone_number} sudah terdaftar."
            )
        
        # Check if email already exists (if provided)
        if user_data.email:
            existing_email = db.query(User).filter(
                User.email == user_data.email
            ).first()
            if existing_email:
                # GANTI ValueError -> HTTPException 400
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email {user_data.email} sudah terdaftar."
                )
        
        # Generate password if not provided
        if not user_data.password:
            if not user_data.birth_date:
                # GANTI ValueError -> HTTPException 400
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tanggal lahir wajib diisi untuk membuat password otomatis. Format password: namadepan + DDMMYYYY"
                )
            
            # Extract first name from full_name
            first_name = user_data.full_name.split()[0].lower()
            
            # Generate password: namadepan + DDMMYYYY
            date_str = user_data.birth_date.strftime("%d%m%Y")
            password = f"{first_name}{date_str}"
        else:
            password = user_data.password
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create user
        user = User(
            password_hash=password_hash,
            full_name=user_data.full_name,
            email=user_data.email,
            phone_number=user_data.phone_number,
            birth_date=user_data.birth_date,
            role=user_data.role,
            kategori_pengguna=user_data.kategori_pengguna,
            is_active=user_data.is_active,
            department_id=user_data.department_id,
            position_id=user_data.position_id,
            work_status_id=user_data.work_status_id,
            company_id=user_data.company_id
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user with username (email or phone_number) and password.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        logger.info(f"🔐 Login attempt with username: {username}")
        
        # Try to find user by email or phone_number
        user = db.query(User).filter(
            (User.email == username) | (User.phone_number == username)
        ).first()
        
        if not user:
            logger.warning(f"❌ User not found: {username}")
            return None
        
        logger.info(f"✅ User found: {user.full_name} (ID: {user.id})")
        
        if not verify_password(password, user.password_hash):
            logger.warning(f"❌ Password mismatch for user: {user.full_name}")
            return None
        
        logger.info(f"✅ Password verified for user: {user.full_name}")
        
        if not user.is_active:
            logger.warning(f"❌ User inactive: {user.full_name}")
            return None
        
        logger.info(f"✅ Login successful: {user.full_name} ({user.role.value})")
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
        """
        Get user by ID.
        """
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with pagination.
        """
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_user(db: Session, user_id: UUID, user_data: UserUpdate) -> User:
        """
        Update user information.
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            # GANTI ValueError -> HTTPException 404 Not Found
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User tidak ditemukan"
            )
        
        # Update fields if provided
        if user_data.full_name is not None:
            user.full_name = user_data.full_name
        
        if user_data.email is not None:
            # Check if email already exists
            existing = db.query(User).filter(
                User.email == user_data.email,
                User.id != user_id
            ).first()
            if existing:
                # GANTI ValueError -> HTTPException 400
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Email {user_data.email} sudah digunakan"
                )
            user.email = user_data.email
        
        if user_data.phone_number is not None:
            # Check if phone already exists
            existing = db.query(User).filter(
                User.phone_number == user_data.phone_number,
                User.id != user_id
            ).first()
            if existing:
                # GANTI ValueError -> HTTPException 400
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Nomor HP {user_data.phone_number} sudah digunakan"
                )
            user.phone_number = user_data.phone_number
        
        if user_data.birth_date is not None:
            user.birth_date = user_data.birth_date
        
        if user_data.role is not None:
            user.role = user_data.role
        
        if user_data.kategori_pengguna is not None:
            user.kategori_pengguna = user_data.kategori_pengguna
        
        if user_data.is_active is not None:
            user.is_active = user_data.is_active
        
        if user_data.department_id is not None:
            user.department_id = user_data.department_id
        
        if user_data.position_id is not None:
            user.position_id = user_data.position_id
        
        if user_data.work_status_id is not None:
            user.work_status_id = user_data.work_status_id
        
        if user_data.company_id is not None:
            user.company_id = user_data.company_id
        
        if user_data.password is not None:
            user.password_hash = hash_password(user_data.password)
        
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> bool:
        """
        Delete a user (soft delete by setting is_active to False).
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # Soft delete
        user.is_active = False
        db.commit()
        
        return True


# Global instance
auth_service = AuthService()
