from typing import List, Dict, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from superset.src.db.models import Product
from superset.src.schemas.products import ProductSchema, ProductCreateSchema


class ProductService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.schema = ProductSchema()
        self.create_schema = ProductCreateSchema()

    def get_all(self) -> List[Dict]:
        try:
            products = self.db.query(Product).all()
            return self.schema.dump(products, many=True)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    def create(self, data: Dict) -> Dict:
        errors = self.create_schema.validate(data)
        if errors:
            raise ValueError(f"Validation error: {errors}")

        try:
            product = Product(**data)
            self.db.add(product)
            self.db.commit()
            self.db.refresh(product)
            return self.schema.dump(product)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    def update(self, product_id: int, data: Dict) -> Optional[Dict]:
        errors = self.create_schema.validate(data, partial=True)
        if errors:
            raise ValueError(f"Validation error: {errors}")

        try:
            product = self.db.query(Product).get(product_id)
            if not product:
                return None

            for key, value in data.items():
                setattr(product, key, value)

            self.db.commit()
            self.db.refresh(product)
            return self.schema.dump(product)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    def delete(self, product_id: int) -> bool:
        try:
            product = self.db.query(Product).get(product_id)
            if not product:
                return False

            self.db.delete(product)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    def get_product_price(self, product_id: int) -> Optional[float]:
        try:
            product = self.db.query(Product).get(product_id)
            if not product:
                return None
            return product.price
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")
