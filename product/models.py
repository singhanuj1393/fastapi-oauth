from database import Base
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products" ## name of database table
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    # Adding foreign key to link product to seller ,
    # Note: sellers is the name of the table in the database, not the name of the model class. The table name is defined in the Seller model class using __tablename__ attribute.
    seller_id = Column(Integer, ForeignKey("sellers.id"))  ## foreign key to link product to seller.

    ## this relationship is used to link the product to the seller who created it. It allows us to access the seller's details from the product and vice versa.
    created_by = relationship("Seller", back_populates="products")  ## relationship to link product to seller

class Seller(Base):
    __tablename__ = "sellers" ## name of database table
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    # this relationship is used to link the seller to the products they have created. It allows us to access the products created by a seller and vice versa.
    products = relationship("Product", back_populates="created_by")  ## relationship to link seller to product