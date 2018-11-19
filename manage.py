from run import app
from models.models import User, Parcel

def create():
    User().create_table()
    Parcel().create_table()

def drop():
    User().drop_table()
    Parcel().drop_table()

def create_admin():
    admin = User(username='AdminUser', email='admin@gmail.com',
                 password='Adminpass123', is_admin=True)
    admin.add()


if __name__ == '__main__':
    with app.app_context():
        drop()
        create()
        create_admin()