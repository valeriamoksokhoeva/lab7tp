from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Category(Base):
    __tablename__ = "Category"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "Product"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("Category.id"))
    category = relationship("Category", back_populates="products")

engine = create_engine("postgresql+psycopg2://username:password@localhost/tpdb")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

#create
category = Category(name="Meat")
product1 = Product(name="Beef", price=890.9, category=category)
product2 = Product(name="Chicken", price=569.4, category=category)

session.add(category)
session.add(product1)
session.add(product2)

session.commit()

#read
category_from_db= session.query(Category).filter_by(name="Meat").first()
print(category_from_db.name, category_from_db.products[0].name, category_from_db.products[0].price)
print(category_from_db.name, category_from_db.products[1].name, category_from_db.products[1].price)

#update
category_from_db.name = "Vegan meat"
session.commit()
print(category_from_db.name, category_from_db.products[0].name, category_from_db.products[0].price)
print(category_from_db.name, category_from_db.products[1].name, category_from_db.products[1].price)

#delete
session.delete(category_from_db)
session.commit()