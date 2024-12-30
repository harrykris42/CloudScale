# src/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import timedelta
from typing import List, Dict
from ....database import get_db
from ....core.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_current_admin_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    verify_password,
    get_password_hash
)
from ....core.session import SessionManager
from ....crud.users import create_user, get_user, update_user, delete_user
from ....schemas.auth import Token, UserCreate, UserRead
from ....models.users import User
import logging
router = APIRouter()
logger = logging.getLogger(__name__)

session_manager = SessionManager("redis://redis:6379/0")

@router.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Find user
        stmt = select(User).where(User.username == form_data.username)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password"
            )

        # Create session
        session_id = await session_manager.create_session({
            "id": user.id,
            "username": user.username,
            "is_admin": user.is_admin
        })

        # Set session cookie
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=86400  # 24 hours
        )

        return {
            "username": user.username,
            "is_admin": user.is_admin,
            "message": "Logged in successfully"
        }

    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.post("/logout")
async def logout(
    response: Response,
    session_id: str = Cookie(None)
):
    if session_id:
        await session_manager.delete_session(session_id)

    response.delete_cookie(key="session_id")
    return {"message": "Logged out successfully"}

@router.get("/me")
async def get_current_user(
    session_id: str = Cookie(None),
    db: AsyncSession = Depends(get_db)
):
    if not session_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    session_data = await session_manager.get_session(session_id)
    if not session_data:
        raise HTTPException(
            status_code=401,
            detail="Session expired"
        )

    # Refresh session
    await session_manager.refresh_session(session_id)

    return session_data

@router.post("/register", response_model=Dict[str, str])
async def register_user(
    email: str,
    username: str,
    password: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Check if user exists
        stmt = select(User).where(
            or_(User.email == email, User.username == username)
        )
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            if existing_user.email == email:
                raise HTTPException(
                    status_code=400,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Username already taken"
                )

        # Create new user
        new_user = User(
            email=email,
            username=username,
            hashed_password=get_password_hash(password)
        )
        db.add(new_user)
        await db.commit()

        return {"message": "Registration successful"}

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    try:
        stmt = select(User).where(User.username == form_data.username)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "is_admin": user.is_admin},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not authenticate user")

@router.get("/users/me", response_model=UserRead)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user

@router.get("/users", response_model=List[UserRead])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    users = await get_users(db, skip=skip, limit=limit)
    return users

@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user_details(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    db_user = await get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await update_user(db, db_user, user_update)
    return updated_user

@router.delete("/users/{user_id}")
async def delete_user_account(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    db_user = await get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")

    await delete_user(db, db_user)
    return {"message": "User deleted successfully"}
