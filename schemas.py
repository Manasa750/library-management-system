from pydantic import BaseModel, Field, constr
from datetime import datetime

# User Schema
class UserCreate(BaseModel):
    username: constr(min_length=8)
    password: constr(min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

# Book Schema
class BookCreate(BaseModel):
    title: str
    author: str
    available_copies: int = Field(ge=1)  # Ensures at least 1 copy is available

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    available_copies: int

    class Config:
        from_attributes = True

# Borrow Request Schema
class BorrowRequest(BaseModel):
    user_id: int
    book_id: int

# Borrow Response Schema
class BorrowResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    return_date: datetime | None

    class Config:
        from_attributes = True
