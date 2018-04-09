from flask_login import UserMixin
from uuid import uuid4
import peewee as pw
from playhouse.db_url import connect
from os import environ
from os.path import abspath
import psycopg2

db = connect(environ.get('DATABASE_URL') or 'sqlite:////' + abspath('dev.db'))

def gen_uuid():
    return uuid4()

def create_db(safe=True):
    print('creating tables...')
    db.create_tables([Node, User], safe=safe) # TODO dry this
    print('tables created')

def populate_db():
    try:
        with db.atomic() as transaction:
            Node.create(lat=55.723533, lon=13.214179, name="magic oval")
            Node.create(lat=55.723367, lon=13.206387, name="mystical clearing")
        print('db populated')
    except pw.IntegrityError:
        print('integrity error when populating db')

# Models

class BaseModel(pw.Model):
    class Meta:
        database = db

class Node(BaseModel):
    id = pw.UUIDField(default=uuid4)
    name = pw.CharField(max_length=80)
    lat = pw.FloatField()
    lon = pw.FloatField()
    def coords() -> tuple:
        return (lat, lon)

class User(BaseModel, UserMixin):
    id = pw.UUIDField(default=uuid4)
    name = pw.CharField(max_length=30, unique=True)
    email = pw.CharField(max_length=254, unique=True) # standard max email length
