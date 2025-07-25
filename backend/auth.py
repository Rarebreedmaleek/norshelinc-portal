from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Security settings
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

# Mock parent database - In production, use a real database
# Pre-computed bcrypt hash for "norshel" to avoid runtime hashing issues
PARENT_DB = {
    "parent1@norshel.com": {
        "email": "parent1@norshel.com",
        "full_name": "John Doe Sr.",
        "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewSBKQNORm7X6E4W",
        "disabled": False
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_parent(email: str):
    """Get parent from database"""
    if email in PARENT_DB:
        parent_dict = PARENT_DB[email]
        return parent_dict
    return None

def authenticate_parent(email: str, password: str):
    """Authenticate a parent"""
    parent = get_parent(email)
    if not parent:
        return False
    if not verify_password(password, parent["hashed_password"]):
        return False
    return parent

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_parent(token: str = Depends(oauth2_scheme)):
    """Get current authenticated parent"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    parent = get_parent(email)
    if parent is None:
        raise credentials_exception
    if parent["disabled"]:
        raise HTTPException(status_code=400, detail="Parent account is disabled")
    return parent 