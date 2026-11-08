from fastapi import APIRouter, Depends, HTTPException, status
from product.models import Product as ProductModel
from product.schemas import Product, ShowProduct,Seller
from sqlalchemy.orm import Session
from fastapi.params import Depends
from database import get_db
from typing import List
from routers.login import get_current_user

router = APIRouter(
    tags=["Products"],
    prefix="/api"  ## this is the prefix for all the endpoints defined in this router. It will be added to the url of all the endpoints defined in this router. For example, if we define an endpoint /product in this router, the url for that endpoint will be /api/product. This is useful when we want to group all the endpoints related to products under a common prefix.
)



## Add the product into the database and return the newly added product as a response.

@router.post("/product",status_code=status.HTTP_201_CREATED) ## we can also define tags for the endpoint here, but it is better to define it at the router level. This way, we can group all the endpoints related to products under the "Products" tag in the documentation. ex: @router.post("/product",status_code=status.HTTP_201_CREATED,tags=["Products"])
def create_product(request: Product, db:Session=Depends(get_db)):
    new_product = ProductModel(
        name=request.name,
        description=request.description,
        price=request.price,
        seller_id=1
    )
    db.add(new_product)
    db.commit() #commit newly added product to database
    db.refresh(new_product) # refresh the database session.
    return new_product

## get all products from the database and return them as a response. 
## use of response_model=List[ShowProduct] to return only the name and price of the product in the response. The description is not included in the response.

@router.get("/products", response_model=List[ShowProduct])
def get_products(db: Session = Depends(get_db),current_user:Seller = Depends(get_current_user)): ## get the current user from the token using the get_current_user function defined in login.py. This will ensure that only authenticated users can access this endpoint.
    products = db.query(ProductModel).all() ## fetch all products from the database
    return products

## get a product by its id from the database and return it as a response. If the product is not found, return an error message.
## use of response_model=ShowProduct to return only the name and price of the product in the response. The description is not included in the response.
@router.get("/product/{product_id}", response_model=ShowProduct)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first() ## fetch the product with the given id from the database
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

## delete a product by its id from the database and return a success message. If the product is not found, return an error message.

@router.delete("/product/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first() ## fetch the product with the given id from the database
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product) ## delete the product from the database
    db.commit() ## commit the changes to the database
    return {"message": "Product deleted successfully"}

# update a product by its id from the database and return a success message. If the product is not found, return an error message.

@router.put("/product/{product_id}")
def update_product(product_id: int, request: Product, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first() ## fetch the product with the given id from the database
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    product.name = request.name
    product.description = request.description
    product.price = request.price
    db.commit() ## commit the changes to the database
    return {"message": "Product updated successfully"}
