import os
from app import create_app
from models.models import User, Parcel

app = create_app(os.getenv("CONFIG_STAGE") or "default")


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

@app.cli.command("db:init")
def db_init():
    create()
    create_admin()

@app.cli.command("db:teardown")
def db_teardown():
    drop()

if __name__ == '__main__':
    app.run(debug=True)