from typing import List, Optional

from sqlalchemy import Column, Date, Float, ForeignKeyConstraint, Integer, LargeBinary, PrimaryKeyConstraint, SmallInteger, String, Table, Text
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()
metadata = Base.metadata


class Categories(Base):
    __tablename__ = 'categories'
    __table_args__ = (
        PrimaryKeyConstraint('category_id', name='pk_categories'),
    )

    category_id = mapped_column(SmallInteger)
    category_name = mapped_column(String(15), nullable=False)
    description = mapped_column(Text)
    picture = mapped_column(LargeBinary)


    products: Mapped[List['Products']] = relationship('Products', uselist=True, back_populates='category')

    def full(self):
        return str(self.category_id) + '. ' + self.category_name + ' (' + str(self.description) + ')'

class CustomerDemographics(Base):
    __tablename__ = 'customer_demographics'
    __table_args__ = (
        PrimaryKeyConstraint('customer_type_id', name='pk_customer_demographics'),
    )

    customer_type_id = mapped_column(String(5))
    customer_desc = mapped_column(Text)

    customer: Mapped['Customers'] = relationship('Customers', secondary='customer_customer_demo', back_populates='customer_type')


class Customers(Base):
    __tablename__ = 'customers'
    __table_args__ = (
        PrimaryKeyConstraint('customer_id', name='pk_customers'),
    )

    customer_id = mapped_column(String(5))
    company_name = mapped_column(String(40), nullable=False)
    contact_name = mapped_column(String(30))
    contact_title = mapped_column(String(30))
    address = mapped_column(String(60))
    city = mapped_column(String(15))
    region = mapped_column(String(15))
    postal_code = mapped_column(String(10))
    country = mapped_column(String(15))
    phone = mapped_column(String(24))
    fax = mapped_column(String(24))

    customer_type: Mapped['CustomerDemographics'] = relationship('CustomerDemographics', secondary='customer_customer_demo', back_populates='customer')
    orders: Mapped[List['Orders']] = relationship('Orders', uselist=True, back_populates='customer')


class Employees(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        ForeignKeyConstraint(['reports_to'], ['employees.employee_id'], name='fk_employees_employees'),
        PrimaryKeyConstraint('employee_id', name='pk_employees')
    )

    employee_id = mapped_column(SmallInteger)
    last_name = mapped_column(String(20), nullable=False)
    first_name = mapped_column(String(10), nullable=False)
    title = mapped_column(String(30))
    title_of_courtesy = mapped_column(String(25))
    birth_date = mapped_column(Date)
    hire_date = mapped_column(Date)
    address = mapped_column(String(60))
    city = mapped_column(String(15))
    region = mapped_column(String(15))
    postal_code = mapped_column(String(10))
    country = mapped_column(String(15))
    home_phone = mapped_column(String(24))
    extension = mapped_column(String(4))
    photo = mapped_column(LargeBinary)
    notes = mapped_column(Text)
    reports_to = mapped_column(SmallInteger)
    photo_path = mapped_column(String(255))

    employees: Mapped[Optional['Employees']] = relationship('Employees', remote_side=[employee_id], back_populates='employees_reverse')
    employees_reverse: Mapped[List['Employees']] = relationship('Employees', uselist=True, remote_side=[reports_to], back_populates='employees')
    territory: Mapped['Territories'] = relationship('Territories', secondary='employee_territories', back_populates='employee')
    orders: Mapped[List['Orders']] = relationship('Orders', uselist=True, back_populates='employee')


class Region(Base):
    __tablename__ = 'region'
    __table_args__ = (
        PrimaryKeyConstraint('region_id', name='pk_region'),
    )

    region_id = mapped_column(SmallInteger)
    region_description = mapped_column(String(60), nullable=False)

    territories: Mapped[List['Territories']] = relationship('Territories', uselist=True, back_populates='region')


class Shippers(Base):
    __tablename__ = 'shippers'
    __table_args__ = (
        PrimaryKeyConstraint('shipper_id', name='pk_shippers'),
    )

    shipper_id = mapped_column(SmallInteger)
    company_name = mapped_column(String(40), nullable=False)
    phone = mapped_column(String(24))

    orders: Mapped[List['Orders']] = relationship('Orders', uselist=True, back_populates='shippers')


class Suppliers(Base):
    __tablename__ = 'suppliers'
    __table_args__ = (
        PrimaryKeyConstraint('supplier_id', name='pk_suppliers'),
    )

    supplier_id = mapped_column(SmallInteger)
    company_name = mapped_column(String(40), nullable=False)
    contact_name = mapped_column(String(30))
    contact_title = mapped_column(String(30))
    address = mapped_column(String(60))
    city = mapped_column(String(15))
    region = mapped_column(String(15))
    postal_code = mapped_column(String(10))
    country = mapped_column(String(15))
    phone = mapped_column(String(24))
    fax = mapped_column(String(24))
    homepage = mapped_column(Text)

    products: Mapped[List['Products']] = relationship('Products', uselist=True, back_populates='supplier')


class UsStates(Base):
    __tablename__ = 'us_states'
    __table_args__ = (
        PrimaryKeyConstraint('state_id', name='pk_usstates'),
    )

    state_id = mapped_column(SmallInteger)
    state_name = mapped_column(String(100))
    state_abbr = mapped_column(String(2))
    state_region = mapped_column(String(50))


t_customer_customer_demo = Table(
    'customer_customer_demo', metadata,
    Column('customer_id', String(5), nullable=False),
    Column('customer_type_id', String(5), nullable=False),
    ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], name='fk_customer_customer_demo_customers'),
    ForeignKeyConstraint(['customer_type_id'], ['customer_demographics.customer_type_id'], name='fk_customer_customer_demo_customer_demographics'),
    PrimaryKeyConstraint('customer_id', 'customer_type_id', name='pk_customer_customer_demo')
)


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], name='fk_orders_customers'),
        ForeignKeyConstraint(['employee_id'], ['employees.employee_id'], name='fk_orders_employees'),
        ForeignKeyConstraint(['ship_via'], ['shippers.shipper_id'], name='fk_orders_shippers'),
        PrimaryKeyConstraint('order_id', name='pk_orders')
    )

    order_id = mapped_column(SmallInteger)
    customer_id = mapped_column(String(5))
    employee_id = mapped_column(SmallInteger)
    order_date = mapped_column(Date)
    required_date = mapped_column(Date)
    shipped_date = mapped_column(Date)
    ship_via = mapped_column(SmallInteger)
    freight = mapped_column(Float)
    ship_name = mapped_column(String(40))
    ship_address = mapped_column(String(60))
    ship_city = mapped_column(String(15))
    ship_region = mapped_column(String(15))
    ship_postal_code = mapped_column(String(10))
    ship_country = mapped_column(String(15))

    customer: Mapped[Optional['Customers']] = relationship('Customers', back_populates='orders')
    employee: Mapped[Optional['Employees']] = relationship('Employees', back_populates='orders')
    shippers: Mapped[Optional['Shippers']] = relationship('Shippers', back_populates='orders')
    order_details: Mapped[List['OrderDetails']] = relationship('OrderDetails', uselist=True, back_populates='order')


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        ForeignKeyConstraint(['category_id'], ['categories.category_id'], name='fk_products_categories'),
        ForeignKeyConstraint(['supplier_id'], ['suppliers.supplier_id'], name='fk_products_suppliers'),
        PrimaryKeyConstraint('product_id', name='pk_products')
    )

    product_id = mapped_column(SmallInteger)
    product_name = mapped_column(String(40), nullable=False)
    discontinued = mapped_column(Integer, nullable=False)
    supplier_id = mapped_column(SmallInteger)
    category_id = mapped_column(SmallInteger)
    quantity_per_unit = mapped_column(String(20))
    unit_price = mapped_column(Float)
    units_in_stock = mapped_column(SmallInteger)
    units_on_order = mapped_column(SmallInteger)
    reorder_level = mapped_column(SmallInteger)

    category: Mapped[Optional['Categories']] = relationship('Categories', back_populates='products')
    supplier: Mapped[Optional['Suppliers']] = relationship('Suppliers', back_populates='products')
    order_details: Mapped[List['OrderDetails']] = relationship('OrderDetails', uselist=True, back_populates='product')


class Territories(Base):
    __tablename__ = 'territories'
    __table_args__ = (
        ForeignKeyConstraint(['region_id'], ['region.region_id'], name='fk_territories_region'),
        PrimaryKeyConstraint('territory_id', name='pk_territories')
    )

    territory_id = mapped_column(String(20))
    territory_description = mapped_column(String(60), nullable=False)
    region_id = mapped_column(SmallInteger, nullable=False)

    employee: Mapped['Employees'] = relationship('Employees', secondary='employee_territories', back_populates='territory')
    region: Mapped['Region'] = relationship('Region', back_populates='territories')


t_employee_territories = Table(
    'employee_territories', metadata,
    Column('employee_id', SmallInteger, nullable=False),
    Column('territory_id', String(20), nullable=False),
    ForeignKeyConstraint(['employee_id'], ['employees.employee_id'], name='fk_employee_territories_employees'),
    ForeignKeyConstraint(['territory_id'], ['territories.territory_id'], name='fk_employee_territories_territories'),
    PrimaryKeyConstraint('employee_id', 'territory_id', name='pk_employee_territories')
)


class OrderDetails(Base):
    __tablename__ = 'order_details'
    __table_args__ = (
        ForeignKeyConstraint(['order_id'], ['orders.order_id'], name='fk_order_details_orders'),
        ForeignKeyConstraint(['product_id'], ['products.product_id'], name='fk_order_details_products'),
        PrimaryKeyConstraint('order_id', 'product_id', name='pk_order_details')
    )

    order_id = mapped_column(SmallInteger, nullable=False)
    product_id = mapped_column(SmallInteger, nullable=False)
    unit_price = mapped_column(Float, nullable=False)
    quantity = mapped_column(SmallInteger, nullable=False)
    discount = mapped_column(Float, nullable=False)

    order: Mapped['Orders'] = relationship('Orders', back_populates='order_details')
    product: Mapped['Products'] = relationship('Products', back_populates='order_details')


#### Now we use the generated models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:example@db/northwind', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

categories = session.query(Categories).all()

for cat in categories:
    print(cat.full())
    for prod in cat.products:
        print('    ---> ',prod.product_name)

#newcat = Categories()
#newcat.category_id = 10
#newcat.category_name = 'Nuova'

#session.add(newcat)
#session.commit()