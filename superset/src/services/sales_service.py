from typing import List, Dict
from datetime import date
from sqlalchemy import func, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from superset.src.db.models import Sale, Product


class SalesService:
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_total_sales(self, start_date: date, end_date: date) -> Dict:
        try:
            total_quantity = self.db.query(func.sum(Sale.quantity)) \
                                    .filter(Sale.date.between(start_date, end_date)) \
                                    .scalar() or 0

            total_amount = self.db.query(func.sum(Sale.quantity * (Product.price - (Product.price * Sale.discount)))) \
                                  .join(Product) \
                                  .filter(Sale.date.between(start_date, end_date)) \
                                  .scalar() or 0

            return {
                "total_quantity": total_quantity,
                "total_amount": round(total_amount, 2)
            }
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

    def get_top_products(self, start_date: date, end_date: date, limit: int = 5) -> List[Dict]:
        try:
            top_products = self.db.query(
                Product.id,
                Product.name,
                func.sum(Sale.quantity).label('total_sold'),
                func.sum(Sale.quantity * (Product.price - (Product.price * Sale.discount))).label('total_revenue')
            ) \
            .join(Sale) \
            .filter(Sale.date.between(start_date, end_date)) \
            .group_by(Product.id, Product.name) \
            .order_by(desc('total_revenue')) \
            .limit(limit) \
            .all()

            return [{
                "product_id": p[0],
                "product_name": p[1],
                "total_sold": p[2],
                "total_revenue": round(p[3], 2)  # округляем до 2 знаков после запятой
            } for p in top_products]
        except SQLAlchemyError as e:
            raise RuntimeError(f"Database error: {str(e)}")

