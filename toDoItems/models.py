from datetime import datetime
from flask import current_app
from toDoItems import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# MODELS FOR CREATING NEW TABLES
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    dob = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False, default='default.png')
    item = db.relationship('Item', backref='person', lazy='dynamic')

    def __repr__(self):
        return f'User({self.fullname}, {self.gender}, {self.dob})'

    # ATTRIBUTES TO WORK WITH LOGIN MANAGER
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.id
    
    # METHODS FOR RESETTING PASSWORD
    def get_reset_token(self, expire_sec=300):
        s = Serializer(current_app.config['SECRET_KEY'], expire_sec)
        token = s.dumps({'user_id':self.id}).decode('utf-8')
        return token

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)



class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(50), nullable=False)
    itemDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'Item({self.itemName},{self.itemDate})'