from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(User):
    username: str
    email: str

    class Config:
        orm_mode = True