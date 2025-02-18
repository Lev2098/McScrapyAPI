import os

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.crud import (
    add_products,
    get_products,
    get_product_by_name,
    get_product_by_id)
from app.database.engine import SessionLocal

import json

from app.database.models.mc_product import McProduct
from app.schemas.mc_product import ProductSchema

router = APIRouter()


def get_db() -> Session:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/parse-menu/")
def parse_menu(file_name: str, db: Session = Depends(get_db)):

    file_path = os.path.join("mcdonalds_scraper", file_name)

    if not os.path.exists(file_path):
        return {"error": f"File with name: {file_name} -> not found."}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            menu_items = json.load(file)
    except FileNotFoundError:
        return {"error": f"File with name: {file_name} -> not found."}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON. Please check the file format."}

    result = add_products(db=db, menu_items=menu_items)
    return {
        "message": "Processing completed!",
        **result
    }


@router.get("/")
def get_all_products(db: Session = Depends(get_db)):

    products = get_products(db)

    if not products:
        return {"message": "No products found."}
    else:
        return [ProductSchema.model_validate(product) for product in products]


@router.get("/{product_name}/")
def get_product_by_name(product_name: str, db: Session = Depends(get_db)):

    product = get_product_by_name(db=db, product_name=product_name)

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product '{product_name}' not found.")

    return {"product": ProductSchema.model_validate(product)}


@router.get("/id/{product_id}/")
def get_product_by_id_route(product_id: int, db: Session = Depends(get_db)):

    product = get_product_by_id(db=db, product_id=product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID '{product_id}' not found. {product}")

    return {"product": ProductSchema.model_validate(product)}


@router.get("/{product_name}/{product_field}/")
def get_product_field(
        product_name: str = None,
        product_field: str = None,
        db: Session = Depends(get_db)
):
    product = db.query(McProduct).filter(
        McProduct.name == product_name).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product '{product_name}' not found."
        )

    if not hasattr(product, product_field):
        raise HTTPException(
            status_code=404,
            detail=f"Field '{product_field}' not found "
                   f"in product '{product_name}'."
        )

    return {product_field: getattr(product, product_field)}
