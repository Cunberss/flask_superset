from typing import List, Dict
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from superset.src.db.models import Category
from superset.src.schemas.categories import CategorySchema, CategoryCreateSchema


class CategoryService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.schema = CategorySchema()
        self.create_schema = CategoryCreateSchema()

    def get_all(self) -> List[Dict]:
        try:
            categories = self.db.query(Category).all()
            return self.schema.dump(categories, many=True)
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    def create(self, data: Dict) -> Dict:
        errors = self.create_schema.validate(data)
        if errors:
            raise ValueError(f"Validation error: {errors}")

        try:
            category = Category(**data)
            self.db.add(category)
            self.db.commit()
            self.db.refresh(category)
            return self.schema.dump(category)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")

    def delete(self, category_id: int) -> bool:
        try:
            category = self.db.query(Category).get(category_id)
            if not category:
                return False

            if category.products:
                raise ValueError("Category has products and cannot be deleted")

            self.db.delete(category)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Database error: {str(e)}")