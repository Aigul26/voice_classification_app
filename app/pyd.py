from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    login: str
    name: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    password_hash: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    login: str | None = None