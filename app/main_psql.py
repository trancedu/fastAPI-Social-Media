from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange 
import psycopg2
from psycopg2.extras import RealDictCursor
import time 
from sqlalchemy.orm import Session
from . import models 
from .database import engine, get_db
from typing import Optional
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True # option to publish or not
    created_at: str = "" # optional rating

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host="localhost", 
                                database="fastapi", 
                                user="postgres", 
                                password="password",
                                cursor_factory=RealDictCursor)    
        cursor = conn.cursor()
        print("Database connected successfully")
        break
    except Exception as error:
        print("Database connection failed")
        print("error: ", error)
        time.sleep(2)
    
@app.get("/") # this directs the browser to the root of the website
async def root():
    # async only used for async functions such as database queries
    return {"message": "Hello World!"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # return {"data": posts}
    return {"status": "success",}

@app.get("/posts") # to retreive posts in the database
def get_posts():
    posts = cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    return [{"data": posts}]


@app.post("/createposts")
def create_posts(post: Post):
    cursor.execute("""
        INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *
                    """, (post.title, post.content))
    # make it not vulnerable to sql injection
    # print(post)
    # return {"data": post.dict()}
    new_post = cursor.fetchone()
    conn.commit() # commit changes to the database when inserting
    return {"post": new_post}

# title str, content str, category str, Bool published


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # response.status_code = status.HTTP_200_OK
    cursor.execute("""select * from posts where id = %s""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit() # commit changes to the database when inserting
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s,  published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return {"data": updated_post}