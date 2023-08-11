from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
        # Opening a schema, opening database to make queries, and getting current user

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()     # Raise an exception if a post dowesn't exist
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(              
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)    # Querying a vote by looking for a post in the vote table by the current user

    found_vote = vote_query.first()     # found_vote is a variable to place a like data that has been found
    # If vote direction = 1 meaning you want to like a post
    # but a vote or like was already made, then raise an exception since already voted
    if (vote.dir == 1):     
        if found_vote:         
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)   # Place a new vote if it doesn't exist
        db.add(new_vote)                                                        # add it
        db.commit()                                                             # commit it
        return {"message": "successfully added a vote"}
    # If vote direction = 0 meaning you want to unlike a post, through an error if vote doesn't exist or delete a post if it exists
    else:                   
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)    # Delete the post if a vote is found
        db.commit()

        return {"message": "successfully deleted vote"}
