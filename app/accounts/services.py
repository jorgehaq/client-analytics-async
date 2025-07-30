from fastapi import HTTPException, status
from app.core.security import verify_password, create_access_token
from app.accounts.models import fake_user_db
from app.accounts.schemas import User, Token, LoginRequest
from datetime import timedelta
from app.core.config import settings

def login_user(login_request: LoginRequest) -> Token:
    user = fake_user_db.get(login_request.username)
    if not user or not verify_password(login_request.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")  
    
    token = create_access_token(data={"sub": user["username"]}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=token, token_type="bearer")
    
def get_user(username: str) -> User:
    user = fake_user_db.get(username)   
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
