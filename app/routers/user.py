from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import List, Optional

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    user.password = utils.hash(user.password)
    
    new_user = models.User(**user.dict()) # ** unpacks the dictionary
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_user) # add the new post to the database
    db.commit() # commit changes to the database when inserting
    db.refresh(new_user) # retrieve the new post from the database and store it in new_post
    return new_user
    
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user

