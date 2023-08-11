
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine 
from app import models
from .routers import post, user, auth, vote
from .config import settings
from pydantic import BaseSettings

# models.Base.metadata.create_all(bind=engine)    # Used to create our models (table in pgsql) once you save the file and main file reloads it will create
                                                # Not needed if alembic is used
app = FastAPI()                 # Creating a fastapi instance      

origins=["*"]      # List of domains API is allowed to commuicate with

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router) # Grab router object from post file and import every path object from that file
app.include_router(user.router) # Grab router object from user file and import every path object from that file
app.include_router(auth.router) # Grab router object from user file and import every path object from that file
app.include_router(vote.router) # Grab router object from vote file and import every path object from that file

@app.get("/")
async def root():
    return {"message": "Hello World from Virginia"}



