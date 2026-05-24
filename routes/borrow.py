from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, crud, database

router = APIRouter()


@router.post("/borrow", response_model=schemas.BorrowResponse)
def borrow_book(borrow_request: schemas.BorrowRequest, db: Session = Depends(database.get_db)):
    return crud.borrow_book(db, borrow_request)


@router.put("/return/{borrow_id}", response_model=schemas.BorrowResponse)
def return_book(borrow_id: int, db: Session = Depends(database.get_db)):
    return crud.return_book(db, borrow_id)