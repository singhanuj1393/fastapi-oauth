from fastapi import APIRouter,status
from product.schemas import Seller, ShowSeller
from product.models import Seller as SellerModel
from sqlalchemy.orm import Session
from fastapi.params import Depends
from database import get_db
from passlib.context import CryptContext


router = APIRouter(
    tags=["Sellers"],
    prefix="/api"  ## this is the prefix for all the endpoints defined in this router.
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



### create a seller in the database and return the newly created seller as a response. If the seller with the same email already exists, return an error message.

@router.post("/seller", status_code=status.HTTP_201_CREATED, response_model=ShowSeller)
def create_seller(request: Seller, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(request.password) ## hash the password before storing it in the database
    new_seller = SellerModel(
        name=request.name,
        email=request.email,
        password=hashed_password
    )
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller