# from fastapi import FastAPI
# from pydantic import BaseModel


# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# app = FastAPI()


# @app.post("/items/")
# async def create_item(item: Item):
#     return item 




from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union, Optional
import json

app = FastAPI()

# Load the JSON file
try:
    with open("db.json", "r") as f:
        db = json.load(f)
except FileNotFoundError:
    db = {}

# Request Model
class ItemIn(BaseModel):
    name: str
    price: float
    tax: float

# update model
class ItemUpdate(BaseModel):
    price: Optional[float] = None
    tax: Optional[float] = None

# Response Model
class ItemOut(BaseModel):
    name: str
    total_price: float

@app.post("/items/", response_model=Union[ItemOut, dict])
def create(item: ItemIn):
    if item.name in db:
        return {"message": "Item already exists"}

    total_price = item.price + item.tax
    db[item.name] = {
        "price": item.price,
        "tax": item.tax,
        "total_price": total_price
    }

    with open("db.json", "w") as f:
        json.dump(db, f, indent=4)

    return {"name": item.name, "total_price": total_price}

#update
@app.put("/items/{name}")
def update_item(name: str, item: ItemUpdate):
    if name not in db:
        raise HTTPException(status_code=404, detail="Item not found")

    # Update only the provided fields
    if item.price is not None:
        db[name]["price"] = item.price
    if item.tax is not None:
        db[name]["tax"] = item.tax

    # Recalculate total price
    db[name]["total_price"] = db[name]["price"] + db[name]["tax"]

    with open("db.json", "w") as f:
        json.dump(db, f, indent=4)

    return {"message": "Item updated", "item": db[name]}

#Remove an item
@app.delete("/items/{name}")
def delete_item(name: str):
    if name not in db:
        raise HTTPException(status_code=404, detail="Item not found")

    deleted_item = db.pop(name)

    with open("db.json", "w") as f:
        json.dump(db, f, indent=4)

    return {"message": "Item deleted", "item": deleted_item}


# from fastapi import FastAPI
# from typing import Optional

# app = FastAPI()


# products = {
#     101: {"name": "Laptop", "price": 50000},
#     102: {"name": "Mobile", "price": 30000},
#     103: {"name": "Tablet", "price": 20000},
#     104: {"name": "Lenovo Laptop", "price": 55000},
# }

# # Path Parameter Example: Fetch product by ID
# @app.get("/products/{item_id}")
# def get_product(item_id: int):
#     if item_id in products:
#         return {"product_id": item_id, "product": products[item_id]}
#     return {"error": "Product not found"}

# # Query Parameter Example: Search products by name
# @app.get("/products/")
# def search_products(q: Optional[str] = None):
#     results = []
#     for product_id, product in products.items():
#         if q and q.lower() in product["name"].lower():
#             results.append({product_id: product})
#     return {"results": results}