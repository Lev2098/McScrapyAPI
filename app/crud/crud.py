from pydantic import ValidationError
from sqlalchemy.orm import Session
from typing import List, Dict, Union
from app.database.models.mc_product import McProduct
from app.schemas.mc_product import UploadProductSchema


def add_products(
        db: Session,
        menu_items: List[Dict]
) -> Dict[str, Union[List[str], str]]:

    added_products = []
    skipped_products = []

    for item in menu_items:
        try:
            validated_product = UploadProductSchema(**item)
        except ValidationError as e:
            skipped_products.append(f"Invalid product with ID: {item.get('id', 'unknown')}. Reason: {e.errors()}")
            continue

        existing_product = db.query(McProduct).filter_by(id=validated_product.id).first()

        if existing_product:
            skipped_products.append(existing_product.title)
            continue


        new_product = McProduct(
            id=validated_product.id,
            title=validated_product.name,
            description=validated_product.description,
            calories=validated_product.calories,
            fats=validated_product.fats,
            carbs=validated_product.carbs,
            proteins=validated_product.proteins,
            unsaturated_fats=validated_product.unsaturated_fats,
            sugar=validated_product.sugar,
            salt=validated_product.salt,
            portion=validated_product.portion
        )
        db.add(new_product)
        added_products.append(new_product.title)

    db.commit()

    return {
        "added": added_products,
        "skipped": skipped_products
    }

def get_products(db: Session):
    return db.query(McProduct).all()