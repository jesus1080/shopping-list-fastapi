from sqlalchemy import Boolean, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(70))
    email = Column(String(70), unique=True)
    password = Column(String(70), unique=True)
    product_list = relationship("ProductList", back_populates="user")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(70))
    price = Column(Float)
    date_creation = Column(Date)
    product_list_id = Column(Integer, ForeignKey("product_list.id"))
    id_provider =  Column(Integer, ForeignKey("providers.id"))
    product_list = relationship("ProductList", back_populates="product")
    product_provider = relationship("Provider", back_populates="product")

class ProductList(Base):
    __tablename__ = 'product_list'

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(70))
    state = Column(Boolean, default=True)
    product = relationship("Product", back_populates="product_list") 
    id_user = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="product_list")

class Provider(Base):
    __tablename__ = 'providers'

    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(70))
    date_creation = Column(Date)
    product = relationship("Product", back_populates="product_provider")

