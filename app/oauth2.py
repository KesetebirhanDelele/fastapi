from datetime import datetime, timedelta
from jose import ExpiredSignatureError, JWTError, jwt
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')  # Login endpoint

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# SECRET_KEY = settings.secret_key
# ALGORITHM = settings.algorithm
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict): # Function takes payload data that the user wants to send and store it for manipulation in the process of authentication
    to_encode = data.copy() # copies data
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})    # This will allow JWT to tell coder when data will expire 
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")   # Extract the id of the token

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)   # Extract data if id matches (validation and extraction)
    except JWTError:
        raise credentials_exception

    return token_data

# Used to pass as a dependency in anyone of path operations so that it takes
# token, verify it and extract id and add it as a parameter to path operations
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):  
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user    

    # return verify_access_token(token, credentials_exception) 
                                                       