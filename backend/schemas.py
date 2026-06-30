from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional


class CreateUser(BaseModel):
    username: str = Field(max_length=100, min_length=3)
    email: EmailStr
    session_id: Optional[str] = None
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    @model_validator(mode="after")
    def validate_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Parollar mos kelmadi")
        return self


class LoginUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class PatchUser(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8)


class ResponseUser(BaseModel):
    username: str
    email: EmailStr
    session_id: str

    class Config:
        from_attributes = True


class UpdateUser(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8)


class DeleteUser(BaseModel):
    password: str
