# module imports
import os

# local imports
from models.models import User,Parcel

from app import create_app

app = create_app("testing")


def migrate():
    """ create test tables """

    User().create_table()
    Parcel().create_table()


def drop():
    """ drop test tables if they exist """
    
    User().drop_table()
    Parcel().drop_table()


def create_admin():
    """ add admin """
    admin = User(username='AdminUser', email='admin@gmail.com',
                 password='Adminpass123', is_admin=True)
    admin.add()

if __name__ == '__main__':
    with app.app_context():
        drop()
        migrate()
        create_admin()