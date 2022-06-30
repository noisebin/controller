''' Quick demo to exercise the new DataEntity module

    Can run without an existing database because one gets created
'''
from fabric.data_entity import DataEntity
import sqlite3
from pprint import pformat

table = 'sprout'
attributes={'id': 'INTEGER PRIMARY KEY NOT NULL', 'description': 'TEXT', 'favourite_food': 'TEXT'}

try:
    veg = DataEntity(name=table, attributes=attributes)
except sqlite3.Warning as e:
    print(f'Error handling {table} data. {e}')
    pass

try:
    veg.store({'description': 'A Rainy Tuesday in Berlin', 'favourite_food': 'Rote Grütze'})
except sqlite3.Warning as e:
    print(f'Error handling {table} data. {e}')
    pass

try:
    result = veg.query('SELECT * FROM sprout')
except sqlite3.Warning as e:
    print(f'Error handling {table} data. {e}')
    pass

print(f'Result was: {pformat(result)}')
