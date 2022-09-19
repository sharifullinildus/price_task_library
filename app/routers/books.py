from fastapi import APIRouter, Depends, HTTPException
import schemas, models
from typing import List
from db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/book/')
def add_book(book: schemas.Book, db:Session = Depends(get_db)):
    pub_id = db.query(models.Publisher).filter(models.Publisher.id == book.publisher).first().id
    authors = db.query(models.Author).filter(models.Author.name.in_(book.authors))
    new_book = models.Book(name=book.name, date=book.date, publisher_id = pub_id)
    new_book.authors = authors
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return 'Book id {new_book.id}'


@router.get('/book/', response_model=List[schemas.Book])
def get_book(req: schemas.GetBook, db: Session = Depends(get_db)):
    book = db.query(models.Book)
    if req.names:
        book = book.filter(models.Book.name.in_(req.names))
    if req.publishers:
        book = book.filter(models.Book.publisher.in_(req.publishers))
    if req.authors:
        book = book.filter(models.Book.authors.any(models.Author.in_(req.authors)))
    return book.limit(req.limit).offset(req.offset).all()


@router.put('/book/')
def update_book(book:schemas.UpdateBook, db:Session = Depends(get_db)):
    upd_book = db.query(models.Book).filter(models.Book.id == book.id).first()
    if not upd_book:
        raise HTTPException(status_code=404, detail='Item not found')
    if book.name:
        upd_book.name = book.name
    if book.date:
        upd_book.date = book.date
    if book.authors:
        authors = db.query(models.Author).filter(models.Author.name.in_(book.authors))
        upd_book.authors = authors
    if book.publisher:
        upd_book.publisher_id = db.query(models.Publisher).filter(models.Publisher.id == book.publisher).first().id
    db.commit()
    return 'Done'