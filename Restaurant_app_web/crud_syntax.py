libraries = """

from sqlalchemy import create_engine
from sqlachemy.orm import sessionmaker
from restdb_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurants.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()

"""

create_syntax_crud = """

myFirstRestaurant = Restaurant(name="Pizza Palace")
sesson.add(myFirstRestaurant)
session.commit()

session.query(Restaurant).all()

cheesepizza = MenuItem(name="Cheese Pizza", description="Made with all ingredients and fresh mozzarella", course="Entree", price="$8.99", restaurant=myFirstRestaurant)
session.add(cheesepizza)
session.commit()

session.query(MenuItem).all()

"""


read_syntax_crud = """

firstResult = session.query(Restaurant).first()
firstResult.name ---> 'Pizza Palace'

items = session.query(MenuItem).all()

for item in items:
	print(item.name)
   
---> All the name on MenuItem

https://docs.sqlalchemy.org/en/14/orm/query.html

"""


update_syntax_crud = """

Steps:
	1. Find Entry -> filter_by()
	2. Reset Values
	3. add to session
	4. session.commit()
	
veggieBurgers = session.query(MenuItem).filter_by(name='Veggie Burger')

for veggieburger in veggieBurgers:
	print(veggieburger.id)
	print(veggieburger.price)
	print(veggieburger.restaurant.name)
	print("\n")
	
	
UrbanVeggieBurger = session.query(MenuItem).filter_by(id=8).one()
print(UrbanVeggieBurger.price) ---> $5.99

UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()

To change every price in veggieBurger is:

for veggieburger in veggieBurgers:
	
	if veggieburger.price != '$2.99':
		veggieburger.price = '$2.99'
		session.add(veggieburger)
		session.commit()

"""


delete_syntax_crud = """

Steps:
	1. Find Entry -> filter_by()
	2. session.delete(entry)
	4. session.commit()
	
	
spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream).one()
session.delete(spinach)
session.commit()

if we use the command again, after the session.commit()

spinach = session.query(MenuItem).filter_by(name='Spinach Ice Cream).one()

we receive a error

raise orm_exc.NoResultFound("No row was found for one()")
sqlalchemy.orm.exc.NoResultFound: No row was found for one()

"""





















