from fastapi import FastAPI

from database import engine
from product.models import Product as ProductModel
from routers import product, seller, login

app = FastAPI(
    title="Product API",
    description="This is a simple Product API built with FastAPI and SQLAlchemy. It allows you to create, read, update, and delete products and sellers.",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Anuj Singh",
        "website": "https://www.google.com/",
        "email": "anuj.singh@example.com"
    },
    #docs_url="/documentation"  ## this is the url where the documentation will be available. By default, it is /docs. You can change it to any url you want.
)

## include product and seller routers in the main application. This allows us to access the endpoints defined in the product and seller routers from the main application.
app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)


ProductModel.metadata.create_all(bind=engine)
