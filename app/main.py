from operator import mod
from statistics import mode
from webbrowser import get
from fastapi import FastAPI, Body, Depends, HTTPException, Request, status
from typing import List
import schemas, models
from db import engine, get_db
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from routers import authors, books, publishers

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(books.router)
app.include_router(publishers.router)
app.include_router(authors.router)
