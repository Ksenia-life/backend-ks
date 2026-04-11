from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user, hash_password, verify_password
from app.database import get_db
from app.repositories import UserRepository
from app.schemas import LoginResponse, UserLogin, UserRegister, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    repository = UserRepository(db)

    existing_user = await repository.get_user_by_username(user_data.username)
    if existing_user is not None:
        raise HTTPException(status_code=400, detail="User already exists")

    user = await repository.create_user(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
    )

    return user


@router.post("/login", response_model=LoginResponse)
async def login_user(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    repository = UserRepository(db)
    user = await repository.get_user_by_username(user_data.username)

    if user is None or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    await repository.login_user(user)

    return {
        "message": "Login successful",
        "user_id": user.id,
    }


@router.post("/logout")
async def logout_user(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = UserRepository(db)
    await repository.logout_user(current_user)

    return {"message": "Logout successful"}