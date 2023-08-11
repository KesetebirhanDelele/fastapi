from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

# Pydantic model for designing FastAPI input and output formats 

class PostBase(BaseModel):      # Defining schema for validation purposes. It defines the shape of a post request and is passed into path operations.
    title: str
    content: str
    published: bool = True      # Default value set to True if user doesn't provide value. This makes it an optional filled

class PostCreate(PostBase):     # Inheritance ensures all features of CreatePost are the same for PostBase
    pass

# Position of UserOut important if it is to be called correctly in the class Post below
class UserOut(BaseModel):   # Schema used to model reponse text for a user login info
    id: int
    email: EmailStr        # Note: password left since we don't want to send the data back to the user
    created_at: datetime
    
    class Config:          # Used to convert sqlalchemy to pydantic model
        orm_mode = True

class Post(PostBase):      # Here you can define which variables to see in response
    id: int                # Not other variables are transferred from basemodel. 
    created_at: datetime   # Only those additional variables listed here 
    owner_id: int
    owner: UserOut         # This ensures all user info is displayed when a get request is made
    
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):    
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):     # Defining schema for the token to allow user to attach token and send for verification
    access_token: str       
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)   # dir=direction of vote 1 when they like a post and 0 when they unlike or have no comment
                        # le=1 means less than or equal to one to allow for 0
                        # Note that 'dir' is a virtaul variable entered in the body of a post to indicate if a post is liked or unliked
                        # For that reason, it is not included in the database model