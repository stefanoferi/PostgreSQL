from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Categories

# Connection to the database

engine = create_engine('postgresql://postgres:example@db/northwind', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Now we use the generated model

categories = session.query(Categories).all()

for cat in categories:
    print(cat.full())
    for prod in cat.products:
        print('    ---> ',prod.product_name)


## Example of adding a new Category
#newcat = Categories()
#newcat.category_id = 10
#newcat.category_name = 'Nuova'

#session.add(newcat) ### --> INSERT
#session.commit() ### --> COMMIT