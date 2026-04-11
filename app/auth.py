import hashlib

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.repositories import UserRepository


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password


async def get_current_user(
    x_user_id: int | None = Header(default=None, alias="X-User-Id"),
    db: AsyncSession = Depends(get_db),
):
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Pass X-User-Id header",
        )

    repository = UserRepository(db)
    user = await repository.get_user_by_id(x_user_id)

    if user is None or not user.is_logged_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authenticated",
        )

    return user