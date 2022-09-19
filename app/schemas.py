from datetime import datetime
from lib2to3.pgen2.token import OP
from pydantic import BaseModel, Field
from typing import Optional, List


class Book(BaseModel):
    id: Optional[int]
    name: str
    date: datetime
    authors: List[str]
    publisher: str

    class Config:
        orm_mode = True

class UpdateBook(BaseModel):
    id: int
    name: Optional[str]
    date: Optional[datetime]
    authors: Optional[List[str]]
    publisher: Optional[str]

    class Config:
        orm_mode = True

class GetBook(BaseModel):
    names: Optional[str]
    authors: Optional[str]
    publishers: Optional[str]
    limit: int = Field(default=20)
    offset: int = Field(default=0)


class Author(BaseModel):
    id: Optional[int]
    name: str
    authbooks: List[Book]


class Publisher(BaseModel):
    id: Optional[int]
    name:str
    pubbooks: List[Book]