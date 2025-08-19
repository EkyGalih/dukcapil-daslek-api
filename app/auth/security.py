from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.user import User


class AuthSettings(BaseSettings):
    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24


auth_settings = AuthSettings()
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(p: str) -> str: return pwd.hash(p)
def verify_password(p: str, h: str) -> bool: return pwd.verify(p, h)


def create_access_token(data: dict, expire_minutes: int | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expire_minutes or auth_settings.JWT_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        auth_settings.JWT_SECRET,
        algorithm=auth_settings.JWT_ALG
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(
            token, auth_settings.JWT_SECRET,
            algorithm=[auth_settings.JWT_ALG]
        )
        sub: str = payload.get("sub")
        if sub is None:
            raise cred_exc
    except JWTError:
        raise cred_exc
    res = await db.execute(select(User).where(User.id == int(sub)))
    user = res.scalar_one_or_none()
    if not user:
        raise cred_exc
    return user


def require_role(*roles: str):
    async def checker(current=Depends(get_current_user)):
        if current.role not in roles:
            raise HTTPException(status_code=403, detail="Insufficient Role")
        return current
    return checker
