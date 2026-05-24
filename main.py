from fastapi import FastAPI,HTTPException,status,Path,Depends
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from routes import users, books, borrow
import models
from models import User
from crud import borrow_book

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(borrow.router, prefix="/borrow", tags=["Borrow"])


@app.get("/")
def read_root():
    return {"message": "Library Management System Running"}


### You need to write for User Delete, Modify Password

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db:Session = Depends(get_db)):
   user_model = db.query(User).filter(User.id == user_id).first()
   if not user_model:
      raise HTTPException(status_code=404, detail="User not found")
# Check if the user has any borrowed books
   borrowed_books = db.query(borrow_book).filter(borrow_book.user_id == user_id).first()
   if borrowed_books:
     raise HTTPException(status_code=400, detail="User has borrowed books and cannot be deleted")
# Delete the user
   db.delete(user_id)
   db.commit()
   return {"message": "User deleted successfully"}

@app.post("/user",status_code=status.HTTP_201_CREATED)
async def create_user(db:Session = Depends(get_db), username: str = "default", password: str = "default", is_admin: bool = False):
   """

   :type db: object
   """
   create_user_model = User(
        id = id,
        username = username,
        password = password,
        is_admin = is_admin
  )
   db.add(create_user_model)
   db.commit()
   db.refresh(create_user_model)
   return{"message": "User created Successfully","User": create_user_model}
