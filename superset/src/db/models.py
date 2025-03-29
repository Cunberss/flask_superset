from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from superset.src.db.base import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)  # Новое поле цены
    category_id = Column(Integer, ForeignKey('categories.id', ondelete="CASCADE"))
    category = relationship("Category", back_populates="products")
    sales = relationship("Sale", back_populates="product", cascade="all, delete-orphan")


class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    discount = Column(Float, nullable=True, default=0.0)
    product = relationship("Product", back_populates="sales")
