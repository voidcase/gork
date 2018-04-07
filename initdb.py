import os
from gorkdata import db, Node

def create_db():
    print('creating database...')
    db.create_all()
    print('database created')

def populate_db():
    db.session.add(Node(lat=55.723533, lon=13.214179, name="magic oval"))
    db.session.add(Node(lat=55.723367, lon=13.206387, name="mystical clearing"))
    db.session.commit()

if __name__ == '__main__':
    create_db()
    populate_db()
