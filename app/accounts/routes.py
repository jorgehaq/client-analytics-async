from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.accounts.schemas import Token, User, LoginRequest
from app.accounts.services import login_user, get_user
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login")

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.post("/login", response_model=Token)
async def login(data: LoginRequest):
    return login_user(data)

    
@router.get("/me", response_model=User)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return get_user(username)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
                            

                    