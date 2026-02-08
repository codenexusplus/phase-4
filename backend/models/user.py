from sqlmodel import SQLModel, Field, Column, DateTime
from typing import Optional
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    __tablename__ = "user"  # Explicitly set table name
    __table_args__ = {'extend_existing': True}  # Allow extending existing table
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str
    created_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow))
    updated_at: datetime = Field(sa_column=Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow))
    is_active: bool = Field(default=True)

class UserCreate(UserBase):
    password: str

class UserLogin(SQLModel):
    email: str
    password: str

class UserUpdate(SQLModel):
    email: Optional[str] = None
    username: Optional[str] = None

class UserPublic(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
