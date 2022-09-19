from fastapi import APIRouter, Depends, HTTPException, Body, Query
import schemas, models
from typing import List
from db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/author/{name}')
def add_author(name:str, db:Session = Depends(get_db)):
    author = models.Author(name=name)
    db.add(author)
    db.commit()
    db.refresh()
    return 'Author id {author.id}'


@router.get('/author/', response_model=List[schemas.Author])
def get_author(names:List[str] = Body(), limit=Query(), offset = Query(), db:Session = Depends(get_db)):
    authors = db.query(models.Author).filter(models.Author.name.in_(names)).limit(limit=limit).offset(offset=offset).all()
    return authors


@router.put('/author/{id}/{name}')
def update_author(id:int, name:str, db: Session = Depends(get_db)):
    author = db.query(models.Author).filter(models.Author.id == id).first()
    if not author:
        raise HTTPException(status_code=404, detail='Not author')
    author.name = name
    db.commit()