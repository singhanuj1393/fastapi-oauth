# Product API

A FastAPI application for registering sellers and managing products. It uses SQLAlchemy with a local SQLite database (`product.db`), and issues bearer tokens for login.

## About

This project is built using **Python, FastAPI, OAuth 2.0, and JWT**. It demonstrates the development of a secure Product API with seller registration, user authentication, login, and token-based authorization.

## Setup and run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
fastapi dev main.py
```

Alternatively, run the app with Uvicorn directly:

```bash
uvicorn main:app --reload
```

The application is available at <http://127.0.0.1:8000>. Interactive API documentation is at <http://127.0.0.1:8000/docs>, and the OpenAPI schema is at <http://127.0.0.1:8000/openapi.json>.

The database URL is `sqlite:///./product.db`. Tables are created when the application starts.

## API routes

All product and seller routes use the `/api` prefix. The login route has no prefix.

| Method | Path | Description | Authentication |
|---|---|---|---|
| `POST` | `/api/seller` | Register a seller; returns the seller's name and email. | None |
| `POST` | `/login` | Authenticate a seller and return an access token. | None |
| `POST` | `/api/product` | Create a product. | None |
| `GET` | `/api/products` | List products (name and price only). | Bearer token |
| `GET` | `/api/product/{product_id}` | Get a product by ID (name and price only). | None |
| `PUT` | `/api/product/{product_id}` | Replace a product's name, description, and price. | None |
| `DELETE` | `/api/product/{product_id}` | Delete a product by ID. | None |

Product routes that look up a specific ID return `404` when the product does not exist. Product creation and seller registration return `201 Created`.

### Register a seller

Send JSON to `POST /api/seller`:

```json
{
  "name": "Example Seller",
  "email": "seller@example.com",
  "password": "choose-a-password"
}
```

The response contains the seller's `name` and `email`, but not the password.

### Log in

Send form-encoded fields `username` and `password` to `POST /login`. The username is the seller's name. A successful response contains an `access_token` and `token_type` (`bearer`).

Use the token in the `Authorization` header when calling `GET /api/products`:

```text
Authorization: Bearer <access_token>
```

Tokens expire after 30 minutes.

### Products

Create and update requests expect JSON with a `name`, a `description`, and a positive numeric `price`, for example:

```json
{
  "name": "Desk lamp",
  "description": "Adjustable LED lamp",
  "price": 39.99
}
```

List and get responses expose only `name` and `price`. The current create route assigns products to seller ID `1`.
