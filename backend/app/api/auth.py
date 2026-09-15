from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

security = HTTPBearer()


@router.post("/register")
def register(
    name: str,
    email: str,
    phone: str,
    password: str,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    password_hash = hash_password(password)

    user = User(
        name=name,
        email=email,
        phone=phone,
        password_hash=password_hash
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "data": {
            "user_id": str(user.id),
            "name": user.name,
            "email": user.email,
            "message": "Registration successful"
        },
        "error": None
    }


@router.post("/login")
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password"
            }
        }

    if not verify_password(
        password,
        user.password_hash
    ):
        return {
            "success": False,
            "data": None,
            "error": {
                "code": "INVALID_CREDENTIALS",
                "message": "Invalid email or password"
            }
        }

    access_token = create_access_token(
        str(user.id)
    )

    return {
        "success": True,
        "data": {
            "user_id": str(user.id),
            "name": user.name,
            "email": user.email,
            "access_token": access_token,
            "token_type": "bearer",
            "message": "Login successful"
        },
        "error": None
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        security
    ),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user_id = decode_access_token(token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


@router.get("/me")
def get_me(
    user: User = Depends(get_current_user)
):
    return {
        "success": True,
        "data": {
            "user_id": str(user.id),
            "name": user.name,
            "email": user.email,
            "phone": user.phone
        },
        "error": None
    }