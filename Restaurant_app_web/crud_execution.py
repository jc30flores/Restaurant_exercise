from unicodedata import name
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restdb_setup import Base, Restaurant, MenuItem
from lotsofmenus import adding_data

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

restaurants = session.query(Restaurant).all()
for r in restaurants:
    print(r.name)


