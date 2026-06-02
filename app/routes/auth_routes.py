from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user_model import User
from app.schemas.user_schema import CreateUser, UserLogin
from app.auth.hash_password import hash_password, verify_password
from app.auth.jwt_handler import create_access_token

router = APIRouter()

#Registering New User
@router.post("/register")
def register_user(
    user: CreateUser,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    hashed_pwd = hash_password(user.password)

    new_user = User(
        username = user.username,
        email = user.email,
        password = hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{"message": "User Registered Successfully"}

@router.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    password_match = verify_password(
        user.password, 
        existing_user.password
    )
    if not password_match:
        raise HTTPException(
            status_code=404,
            detail="Invalid credentials"
        )
    
    access_token = create_access_token(
        data={
            "sub": str(existing_user.user_id),
            "email": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
