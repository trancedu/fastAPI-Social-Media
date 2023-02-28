from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote



models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware, # a function that performs operations on the request and response
    allow_origins=origins, # allow all origins
    allow_credentials=True, 
    allow_methods=["*"], # allow all HTTP methods
    allow_headers=["*"], # allow all headers
)
    

app.include_router(post.router) # find matches in the router
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") # this directs the browser to the root of the website
async def root():
    # async only used for async functions such as database queries
    return {"message": "Hello World!"}



