from fastapi import APIRouter, status,HTTPException,Depends
from product.schemas import Login
from product import models, schemas
from database import get_db
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta,timezone
from jose import jwt,JWTError

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from product.schemas import TokenData


router = APIRouter()

SECRET_KEY = "91d0739b0405b15de95311bd68666a7d94e62e4bf42200f2415fcbc218d5c847"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
        token_data = TokenData(username=username)
        return token_data
    except JWTError:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.name == request.username).first()
    if not seller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username") ## if the seller with the given username is not found in the database, raise an HTTPException with status code 404 (Not Found) and a detail message "Invalid username".
   
    if not pwd_context.verify(request.password, seller.password): ## verify the password using the hashed password stored in the database. If the password is incorrect, raise an HTTPException with status code 401 (Unauthorized) and a detail message "Invalid password".
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")  
    access_token = create_access_token(data={"sub": seller.name}) ## create an access token for the seller using the create_access_token function defined below. The access token is created using the seller's name as the subject (sub) of the token.
    return {"access_token": access_token, "token_type": "bearer"} ## return the access token




