from sqlalchemy.orm import Session
from superset.src.db.models import Category, Product, Sale
from datetime import datetime, timedelta
from superset.src.db.base import get_session
import random


def seed_data(session: Session):

    session.query(Sale).delete()
    session.query(Product).delete()
    session.query(Category).delete()
    session.commit()

    # Создаем категории
    categories = [
        Category(name="Electronics"),
        Category(name="Clothing"),
        Category(name="Books")
    ]
    session.add_all(categories)
    session.commit()

    # Данные для продуктов
    products_data = {
        "Electronics": ["Laptop", "Smartphone", "Headphones", "Smart Watch", "Tablet", "Camera"],
        "Clothing": ["T-shirt", "Jeans", "Jacket", "Dress", "Sneakers", "Hat"],
        "Books": ["Novel", "Science Fiction", "Biography", "History Book", "Cookbook", "Poetry Collection"]
    }

    products = []
    for category in categories:
        for product_name in products_data.get(category.name, []):
            price = round(random.uniform(10, 200), 2)
            products.append(Product(
                name=product_name,
                price=price,
                category_id=category.id
            ))

    session.add_all(products)
    session.commit()

    for product in products:
        for i in range(180):
            date = datetime.now() - timedelta(days=i)
            discount = round(random.uniform(0, 0.3), 2) if random.random() > 0.7 else 0.0
            session.add(Sale(
                product_id=product.id,
                quantity=random.randint(1, 10),
                date=date,
                discount=discount
            ))

    session.commit()


def main():
    with get_session() as session:
        seed_data(session)


if __name__ == '__main__':
    main()