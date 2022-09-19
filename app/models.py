from ast import For
from msilib import Table
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import DateTime, Integer, String
from sqlalchemy.orm import relationship, backref
from db import Base

books_authors = Table(
    'books_authors',
    Base.metadata,
    Column('book_id', ForeignKey('books.id')),
    Column('author_id', ForeignKey('authors.id'))
)

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, nullable=False, index = True)
    name = Column(String, nullable = False)
    publisher_id = Column(Integer, ForeignKey('publishers.id'), nullable=False)
    date = Column(DateTime)

    publisher = relationship('Publisher', back_populates='pubbooks')
    authors = relationship('Author', secondary=books_authors, back_populates='authbooks')

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable =False)

    authbooks = relationship('Book', secondary = books_authors, back_populates='authors')

class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable =False)

    pubbooks = relationship('Book', back_populates='publisher')


