from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, constr
from typing import List
from db import db

app = FastAPI()

class ProductIn(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    category: constr(strip_whitespace=True, min_length=1)
    quantity: int = Field(..., ge=0)
    price: float = Field(..., ge=0)

class Product(ProductIn):
    id: int
    created_at: str

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

@app.post("/products", response_model=Product, status_code=201)
async def add_product(product: ProductIn):
    try:
        prod = await db.add_product(
            product.name, product.category, product.quantity, product.price
        )
        return prod
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@app.get("/products", response_model=List[Product])
async def list_products():
    products = await db.list_products()
    return products
