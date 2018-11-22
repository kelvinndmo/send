import psycopg2
from flask import current_app
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash


class SendITDB:
    def __init__(self):
        self.db_name = current_app.config.get('DB_NAME')
        self.db_host = current_app.config.get('DB_HOST')
        self.db_user = current_app.config.get('DB_USER')
        self.db_password = current_app.config.get('DB_PASSWORD')

        self.connection = psycopg2.connect(
            database=self.db_name,
            host=self.db_host,
            user=self.db_user,
            password=self.db_password
        )

        self.cursor = self.connection.cursor()

class User(SendITDB):
    def __init__(self, username=None, email=None, password=None, is_admin=False):
        super().__init__()
        self.username = username
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        self.is_admin = is_admin

    def create_table(self):
        self.cursor.execute(
             '''
            CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                username VARCHAR NOT NULL UNIQUE,
                email VARCHAR NOT NULL UNIQUE,
                password VARCHAR NOT NULL,
                is_admin VARCHAR NOT NULL
            )
            '''
        )
        self.connection.commit()
        self.cursor.close()

    def drop_table(self):
        self.cursor.execute(
            '''DROP TABLE IF EXISTS users'''
        )
        self.connection.commit()
        self.cursor.close()

    def add(self):
        '''add user to user table'''
        self.cursor.execute(
            '''INSERT INTO users(username,email,password,is_admin) VALUES(%s, %s, %s, %s)''',
            (self.username, self.email, self.password, self.is_admin)
        )

        self.connection.commit()
        self.cursor.close()

    def get_by_id(self, id):
        '''get user by id'''
        self.cursor.execute('''SELECT * FROM users WHERE id=%s''',
                            (id, ))
        user = self.cursor.fetchone()

        self.connection.commit()
        self.cursor.close()

        if user:
            return self.objectify_user(user)
        return None


    def get_by_username(self, username):
        '''get user by username'''
        self.cursor.execute('''SELECT * FROM users WHERE username=%s''',
                            (username, ))
        user = self.cursor.fetchone()

        self.connection.commit()
        self.cursor.close()

        if user:
            return self.objectify_user(user)
        return None

    def get_user_by_email(self, email):
        '''get user by email'''
        self.cursor.execute('''SELECT * FROM users WHERE email=%s''',
                            (email,))

        user = self.cursor.fetchone()

        self.connection.commit()
        self.cursor.close()

        if user:
            return self.objectify_user(user)
        return None

    def serialize(self):
        '''return an object as dictionary'''
        return dict(
            username=self.username,
            email=self.email,
            is_admin=self.is_admin
        )

    def objectify_user(self, data):
        '''coerse a tuple into an object'''

        self.id = data[0]
        self.username = data[1]
        self.email = data[2]
        self.password = data[3]
        self.is_admin = data[4]

        return self


class Parcel(SendITDB):
    def __init__(self, sender=None, origin=None, current_location=None, destination=None, price=None, weight=None, status="Pending"):
        super().__init__()
        self.sender = sender
        self.origin = origin
        self.current_location = current_location
        self.destination = destination
        self.price = price
        self.weight = weight
        self.status = status
        self.date = str(datetime.now())
    
    def create_table(self):
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS parcels(
                id serial PRIMARY KEY,
                sender VARCHAR NOT NULL,
                origin VARCHAR NOT NULL,
                current_location VARCHAR NOT NULL,
                destination VARCHAR NOT NULL,
                price INT NOT NULL,
                weight VARCHAR NOT NULL,
                status VARCHAR NOT NULL,
                date TIMESTAMP
            )
            '''
        )
        self.connection.commit()
        self.connection.close()

    def drop_table(self):
        self.cursor.execute(
            '''
            DROP TABLE IF EXISTS parcels
            '''
        )
        self.connection.commit()
        self.connection.close()


    def add(self):
        '''add parcel order to database'''
        self.cursor.execute(
            '''INSERT INTO parcels(sender, origin, current_location, destination,price,weight,status,date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',
            (self.sender, self.origin, self.current_location, self.destination, self.price, self.weight, self.status, self.date)
        )

        self.connection.commit()
        self.connection.close()

    def get_by_id(self, order_id):
        '''fetch an order by id'''
        self.cursor.execute(
            '''SELECT * FROM parcels WHERE id=%s''',
            (order_id, )
        )

        order = self.cursor.fetchone()

        self.connection.commit()
        self.cursor.close()

        if order:
            return self.objectify(order)
        return None
    def mark_in_transit(self, order_id):
        '''mark an order as in transit after being approved'''
        self.cursor.execute(
            '''UPDATE parcels SET status=%s WHERE id=%s''',
            ('In Transit', order_id)
        )
        
        self.connection.commit()
        self.cursor.close()

    def delete(self, order_id):
        '''delete parcel order'''
        self.cursor.execute('''DELETE FROM parcels WHERE id=%s ''',
                            (order_id, ))

        self.connection.commit()
        self.cursor.close()

    def accept_status(self, order_id):
        '''accept an order'''
        self.cursor.execute(
            """UPDATE parcels SET status=%s WHERE id=%s
            """, ('accepted', order_id)

        )

        self.connection.commit()
        self.cursor.close()

    def decline_order(self, order_id):
        """decline a specific order"""
        self.cursor.execute(
            """UPDATE parcels SET status=%s WHERE id=%s
            """, ('declined', order_id)
        )

        self.connection.commit()
        self.cursor.close()
    
    def cancel_order(self, order_id):
        """cancel a specific order by id"""
        self.cursor.execute(
            "UPDATE parcels SET status=%s WHERE id=%s",
            ('canceled',order_id)
        )

        self.connection.commit()
        self.cursor.close()

    def complete_accepted_order(self, order_id):
        """mark an order as completed"""
        self.cursor.execute(
            """UPDATE parcels SET status=%s WHERE id=%s
            """, ('completed', order_id)

        )

        self.connection.commit()
        self.cursor.close()

    def get_all_orders(self):
        """ get all placed parcel orders"""
        self.cursor.execute("SELECT * FROM parcels ORDER BY id")

        orders = self.cursor.fetchall()
        self.connection.commit()
        self.cursor.close()

        if orders:
            return [self.objectify(order) for order in orders]
        return None

    def orders_by_sender(self, sender):
        ''' Get orders from the same sender'''
        self.cursor.execute(
            """SELECT * FROM parcels WHERE sender=%s""",
            (sender, )
        )

        orders_from_specific_sender = self.cursor.fetchall()

        self.connection.commit()
        self.cursor.close()

        if orders_from_specific_sender:
            return [
                self.objectify(accepted_order)
                for accepted_order in orders_from_specific_sender
            ]
        return None

    def accepted_orders(self):
        ''' Get orders accepted by admin'''
        self.cursor.execute(
            """SELECT * FROM parcels WHERE status=%s""",
            ('accepted', )
        )

        accepted_orders = self.cursor.fetchall()

        self.connection.commit()
        self.cursor.close()

        if accepted_orders:
            return [
                self.objectify(accepted_order)
                for accepted_order in accepted_orders
            ]
        return None

    def declined_orders(self):
        '''return declined orders'''
        self.cursor.execute(
            """SELECT * FROM parcels WHERE status=%s""",
            ('declined',)
        )

        declined_orders = self.cursor.fetchall()

        self.connection.commit()
        self.cursor.close()

        if declined_orders:
            return [
                self.objectify(declined_order)
                for declined_order in declined_orders
            ]
        return None

    def update_location(self, parcel_id):
        ''' update parcel location'''
        self.cursor.execute("""
        UPDATE parcels SET current_location=%s WHERE id=%s
        """, (self.current_location, parcel_id)
        )
        self.connection.commit()
        self.cursor.close()

    def update_destination(self, parcel_id):
        ''' update parcel destination'''
        self.cursor.execute("""
        UPDATE parcels SET destination=%s WHERE id=%s
        """, (self.destination, parcel_id)
        )
        self.connection.commit()
        self.cursor.close()


    def intransit_orders(self):
        '''get orders in transit'''
        self.cursor.execute(
            "SELECT * FROM parcels WHERE status=%s",
            ('In Transit',)
            )
        
        intransit_orders = self.cursor.fetchall()
        
        self.connection.commit()
        self.cursor.close()

        if intransit_orders:
            return [
                self.objectify(intransit_order)
                for intransit_order in intransit_orders
            ]
        return None

    def completed_orders(self):
        '''get all completed orders'''
        self.cursor.execute(
            """SELECT * FROM parcels WHERE status=%s""",
            ('completed',)
        )

        completed_orders = self.cursor.fetchall()

        self.connection.commit()
        self.cursor.close()

        if completed_orders:
            return [
                self.objectify(completed_order)
                for completed_order in completed_orders
            ]
        return None

    def json_order(self):
        '''return an object as dictionary'''
        return dict(
            sender=self.sender,
            origin=self.origin,
            current_location=self.current_location,
            destination=self.destination,
            weight=self.weight,
            status=self.status,
            price=self.price,
            date=self.date
        )


    def serialize(self):
        '''return an object as dictionary'''
        return dict(
            id=self.id,
            sender=self.sender,
            origin=self.origin,
            current_location=self.current_location,
            destination=self.destination,
            weight=self.weight,
            status=self.status,
            price=self.price,
            date=self.date
        )

    def objectify(self, data):
        '''map a tuple to an object'''
        order = Parcel(
            sender=data[1],
            origin=data[2],
            current_location=data[3],
            destination=data[4],
            price=data[5],
            weight=data[6],
            status=data[7])
        order.id = data[0]
        order.date = str(data[8])

        self = order
        return self
