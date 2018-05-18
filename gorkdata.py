from flask_login import UserMixin
from uuid import uuid4
import peewee as pw
from playhouse.db_url import connect
from os import environ
from os.path import abspath
import psycopg2
from config import *

# indices in coordinates tuple
LAT = 0 # y
LON = 1 # x

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
    name = pw.CharField(max_length=NODENAME_MAX_LENGTH)
    lat = pw.FloatField()
    lon = pw.FloatField()
    def coords(self) -> tuple:
        return (self.lat, self.lon)

class User(BaseModel, UserMixin):
    id = id_field()
    name = pw.CharField(max_length=USERNAME_MAX_LENGTH, unique=True)
    email = pw.CharField(max_length=EMAIL_MAX_LENGTH, unique=True) # standard max email length
    password_hash = pw.TextField()
    
    @staticmethod
    def get_by_name(n):
        return User.get(User.name == n)

    @staticmethod
    def get_by_name_or_none(n):
        return User.get_or_none(User.name == n)

    @staticmethod
    def register(name,email,pw):
        from werkzeug.security import generate_password_hash
        return User.create(
                name=name,
                email=email,
                password_hash=generate_password_hash(data)
                )

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
        # Node.create(lat=55.723533, lon=13.214179, name="magic oval")
        # Node.create(lat=55.723367, lon=13.206387, name="mystical clearing")
        User.register(name='Aaa',email='aaa@aaa.aaa',pw='a'*9)
    print('db populated')

def reset_db():
    create_db(purge=True)
    # populate_db()
