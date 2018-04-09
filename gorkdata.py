from flask_login import UserMixin
from uuid import uuid4
import peewee as pw
from playhouse.db_url import connect
from os import environ
from os.path import abspath
import psycopg2

db = connect(environ.get('DATABASE_URL') or 'sqlite:////' + abspath('dev.db'))


def gen_id() -> str:
    return str(uuid4())


def id_field():
    return pw.CharField(max_length=40, primary_key=True, default=gen_id)


# Models


class BaseModel(pw.Model):
    class Meta:
        database = db

class Node(BaseModel):
    id = id_field()
    name = pw.CharField(max_length=80)
    lat = pw.FloatField()
    lon = pw.FloatField()
    def coords() -> tuple:
        return (lat, lon)

class User(BaseModel, UserMixin):
    id = id_field()
    name = pw.CharField(max_length=30, unique=True)
    email = pw.CharField(max_length=254, unique=True) # standard max email length

ALL_TABLES = [Node, User]

# init stuff

def create_db(purge=False):
    if purge:
        print('dropping tables')
        db.drop_tables(ALL_TABLES)
    print('creating tables...')
    db.create_tables(ALL_TABLES) # TODO dry this
    print('tables created')


def populate_db():
    with db.atomic() as transaction:
        Node.create(lat=55.723533, lon=13.214179, name="magic oval")
        Node.create(lat=55.723367, lon=13.206387, name="mystical clearing")
    print('db populated')
