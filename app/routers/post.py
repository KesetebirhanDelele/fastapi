from typing import List, Optional
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int=10, skip: int=0, search: Optional[str] =""):

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # Use below code to limit users to view their own posts only 
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() 

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id,**post.dict())    # Short version

    db.add(new_post)        # add data
    db.commit()             # commit change
    db.refresh(new_post)    # retrieve data

    return new_post            # This will print post in Web/Postman

@router.get("/latest", response_model=schemas.Post)                   # Order matters since if you put this function below "/posts/{id}", it will be invalid
def get_latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):                      # since it will throw an error since this is not an integer
    posts = db.query(models.Post).all()

    # Use below code to limit users to view their own posts only 
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    return posts[-1]
    
@router.get("/{id}", response_model=schemas.Post)                     # Path parameters will always be string
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):                      # input validation to make input integer. That will throw an error if input is string 

    post = db.query(models.Post).filter(models.Post.id == id).first()    
    
    # Use below code to limit users to view their own posts only 
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,          # Same output as the two rows commented out below but simpler
                            detail=f"post with id: {id} was not found")
    
    # if post.owner_id != current_user.id:        # Throwing an error message if a user tries to delete post of another user 
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:           # Throwing an error message if a post doesn't exist 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform this')
    
    if post.owner_id != current_user.id:        # Throwing an error message if a user tries to delete post of another user 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post) # User requests to update a record by indicating the id
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):   # int id taken and data placed in json body taken to post place holder

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post= post_query.first()

    if post == None:           # Throwing an error message if an index doesn't exist 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')

    if post.owner_id != current_user.id:            # Throwing an error message if a user tries to update post of another user 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()