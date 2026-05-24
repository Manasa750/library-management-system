from sqlalchemy.orm import Session

from auth import hash_password
from datetime import datetime, timedelta
from auth import hash_password
from fastapi import HTTPException
import schemas,models


# Register a user
def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session):
    return db.query(models.User).all()


# Add a book
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# Borrow a book
def borrow_book(db: Session, borrow_request: schemas.BorrowRequest):
    book = db.query(models.Book).filter(models.Book.id == borrow_request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_copies < 1:
        raise HTTPException(status_code=400, detail="No available copies")

    # Check if the user has already borrowed this book and not returned it
    existing_borrow = (
        db.query(models.BorrowedBook)
        .filter(
            models.BorrowedBook.user_id == borrow_request.user_id,
            models.BorrowedBook.book_id == borrow_request.book_id,
            models.BorrowedBook.return_date == datetime.now() + timedelta(days=7)
        )
        .first()
    )
    if existing_borrow:
        raise HTTPException(status_code=400, detail="You have already borrowed this book")

    # Proceed with borrowing
    borrowed_book = models.BorrowedBook(user_id=borrow_request.user_id, book_id=borrow_request.book_id)
    book.available_copies -= 1  # Reduce available copies
    db.add(borrowed_book)
    db.commit()
    db.refresh(borrowed_book)
    return borrowed_book


# Return a book
def return_book(db: Session, borrow_id: int):
    borrowed_book = db.query(models.BorrowedBook).filter(models.BorrowedBook.id == borrow_id).first()
    if not borrowed_book:
        raise HTTPException(status_code=404, detail="Borrow record not found")

    if borrowed_book.return_date:
        raise HTTPException(status_code=400, detail="Book already returned")

    # Update return date and increase available copies
    borrowed_book.return_date = datetime.utcnow()
    book = db.query(models.Book).filter(models.Book.id == borrowed_book.book_id).first()
    if book:
        book.available_copies += 1

    db.commit()
    db.refresh(borrowed_book)
    return borrowed_book