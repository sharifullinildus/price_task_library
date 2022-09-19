from fastapi import APIRouter, Depends, HTTPException, Body, Query
import schemas, models
from typing import List
from db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/publisher/{name}')
def add_publisher(name:str, db:Session = Depends(get_db)):
    publisher = models.Publisher(name=name)
    db.add(publisher)
    db.commit()
    db.refresh()
    return 'Publisher id {publisher.id}'


@router.get('/publisher/', response_model=List[schemas.Publisher])
def get_publisher(names:List[str] = Body(), limit=Query(), offset = Query(), db:Session = Depends(get_db)):
    publisher = db.query(models.Publisher).filter(models.Publisher.name.in_(names)).limit(limit=limit).offset(offset=offset).all()
    return publisher


@router.put('/publisher/{id}/{name}')
def update_publisher(id:int, name:str, db: Session = Depends(get_db)):
    publisher = db.query(models.Publisher).filter(models.Publisher.id == id).first()
    if not publisher:
        raise HTTPException(status_code=404, detail='Not publisher')
    publisher.name = name
    db.commit()