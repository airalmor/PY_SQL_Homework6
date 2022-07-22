import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale
import json


DSN = 'postgresql://postgres:postgres@localhost:5432/netology_db'

engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()
con = engine.connect()
create_tables(engine)

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)
for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

res = input('Введите издателя: ')
query_2 = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.id == res)
query_3 = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name == res)
shops = []

try:
    res = int(res)
    result = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.id == res)
except ValueError:
    result = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name == res)
for i in result:
    shops.append(i.name)

print(f"Книги издателя {res} продаются в магазинах: {','.join(shops)}")

session.close()
