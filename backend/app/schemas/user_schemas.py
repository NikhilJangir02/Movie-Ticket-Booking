from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str

class UserUpdate(BaseModel):
    name: str
    email: EmailStr

class ChangePassword(BaseModel):
    current_password: str
    new_password: str    