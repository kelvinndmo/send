from run import app


if __name__ == '__main__':
    with app.app_context():
        drop()
        create()
        create_admin()