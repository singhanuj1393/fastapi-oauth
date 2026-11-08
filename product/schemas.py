from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class Product(BaseModel):
    name: str = Field(..., description="The name of the product")
    description: str = Field(..., description="A brief description of the product")
    price: float = Field(..., gt=0, description="The price of the product, must be greater than 0")

## this schema is used to show the product details in the response. It only includes the name and price of the product. The description is not included in the response.
class ShowProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str 
    price: float

class Seller(BaseModel):
    name: str = Field(..., description="The name of the seller")
    email: str = Field(..., description="The email of the seller")
    password: str = Field(..., description="The password of the seller")

class ShowSeller(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: str 

class Login(BaseModel):
    username: str = Field(..., description="The username of the user")
    password: str = Field(..., description="The password of the user")


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    
