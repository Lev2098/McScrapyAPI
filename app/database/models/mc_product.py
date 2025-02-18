from sqlalchemy import Column, Integer, String, Float
from app.database.engine import Base


class McProduct(Base):
    __tablename__ = "mc_product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    calories = Column(Integer)
    fats = Column(Float)
    carbs = Column(Float)
    proteins = Column(Float)
    unsaturated_fats = Column(Float)
    sugar = Column(Float)
    salt = Column(Float)
    portion = Column(Integer)
