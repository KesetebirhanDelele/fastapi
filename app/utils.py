from passlib.context import CryptContext    # Importing encryption library
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")     # Telling paslib what hashing algorithm we want to use which is 'bcrypt'

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

