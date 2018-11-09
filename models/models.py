from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

orders = []
Users = []
user_orders = []
destinations = ['keroka', 'kisii', 'Nairobi',
                'ogembo', 'mombasa', 'nakuru', 'kisumu', 'kiambu']


class User:
    
    user_id = 1

    def __init__(self,  username=None, email=None, password=None,
                 is_admin=None):
        super().__init__()
        self.username = username
        self.email = email
        if password:
            self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin
        self.id = User.user_id

        User.user_id += 1

    def get_by_username(self, username):
        for user in Users:
            if user.username == username:
                return user

    def get_by_email(self, email):
        for user in Users:
            if user.email == email:
                return user
    



class Order:

    order_id = 1

    def __init__(self, origin=None, price=None, destination=None, weight=None, status="Pending"):
        super().__init__()
        self.origin = origin
        self.price = price
        self.destination = destination
        self.weight = weight   
        self.id = Order.order_id
        self.date = datetime.now().replace(second=0, microsecond=0)
        self.status = status

        Order.order_id += 1
        

    def serialize(self):
        '''returns a tuple as dictionary'''
        return dict(
            id=self.id,
            origin=self.origin,
            price=self.price,
            destination=self.destination,
            weight=self.weight,
            status=self.status,
            user_id=get_jwt_identity(),
            date_placed=str(self.date),
        )

    def get_by_id(self, order_id):
        '''get a single item by unique id'''

        for order in orders:
            if order.id == order_id:
                return order




