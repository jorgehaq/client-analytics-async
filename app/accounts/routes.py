from fastapi import APIRouter, Depends
from app.accounts.schemas import Token, UserResponse, LoginRequest
from app.accounts.services import login_user, get_current_user
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.post("/login", response_model=Token)
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, data)
    
@router.get("/me", response_model=UserResponse)
async def get_me(user=Depends(get_current_user)):
    return user
