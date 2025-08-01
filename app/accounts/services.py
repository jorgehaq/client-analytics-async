from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta
from sqlalchemy.orm import Session

from app.accounts.schemas import Token, LoginRequest
from app.core.config import settings
from app.core.models import User
from app.core.security import verify_password, create_access_token
from app.core.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login")


def login_user(db: Session, login_request: LoginRequest) -> Token:
    user = db.query(User).filter(User.username == login_request.username).first()
    if not user or not verify_password(login_request.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")  
    
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
    
def get_user(db: Session, user_id: str) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
 

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(payload)
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return get_user(db, user_id)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
