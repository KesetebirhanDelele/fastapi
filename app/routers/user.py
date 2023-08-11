from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)): # user is a place holder that will validate input
    
    # create the hash of the password (new.password) before creating the user
    hashed_password = utils.hash(user.password)      # Create a hash for the user password and stoe it
    user.password = hashed_password     # Update the pydantic user model with hashed password
    new_user = models.User(**user.dict())    
        
    db.add(new_user)        # add data
    db.commit()             # commit change
    db.refresh(new_user)    # retrieve data

    return new_user         # This will print post in Web/Postman

@router.get("/{id}", response_model=schemas.UserOut)                     # Path parameters will always be string
def get_user(id: int, db: Session = Depends(get_db)):
    # first specifies that we stop seraching when we get the first match since only one record is expected
    user = db.query(models.User).filter(models.User.id == id).first()        
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,          # Same output as the two rows commented out below but simpler
                            detail=f"user with id: {id} was not found")  
    return user