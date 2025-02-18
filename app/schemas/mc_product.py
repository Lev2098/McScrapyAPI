from pydantic import BaseModel, validator


class UploadProductSchema(BaseModel):
    id: int
    name: str
    description: str = "No description provided."
    calories: int = 0
    fats: float = 0.0
    carbs: float = 0.0
    proteins: float = 0.0
    unsaturated_fats: float = 0.0
    sugar: float = 0.0
    salt: float = 0.0
    portion: int = 0

    @validator(
        "calories",
        "fats",
        "carbs",
        "proteins",
        "unsaturated_fats",
        "sugar",
        "salt",
        pre=True,
        always=True
    )
    def validate_numeric_fields(cls, value):
        try:
            return float(value) if "." in str(value) else int(value)
        except (ValueError, TypeError):
            return 0.0 if isinstance(value, str) and "." in value else 0


class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    calories: int
    fats: float
    carbs: float
    proteins: float
    unsaturated_fats: float
    sugar: float
    salt: float
    portion: int

    model_config = {
        "from_attributes": True,
    }
