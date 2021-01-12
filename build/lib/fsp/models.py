from fsp import db, app,login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# ritorna un user partendo dal suo ID

class User (db.Model, UserMixin):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    volunteer = db.Column(db.Boolean(), nullable=False)
    phone=db.Column(db.String(10), nullable=False)
    bonus=db.Column(db.Integer,nullable=False)
    order=db.relationship('Order', back_populates = 'user',lazy = True)
    point_bonus = db.relationship('Bonus', back_populates='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Point (db.Model):
    __tablename__ = 'points'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64), unique=True)
    city= db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(64), nullable=False, unique=True)

class FoodAvailable(db.Model):
    __tablename__ = 'food available'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)  #aumenta l'id
    type = db.Column(db.String())
    expired_data=db.Column(db.DateTime)
    point= db.Column(db.String(64), db.ForeignKey('points.name'))
    availability=db.Column(db.Integer, nullable=False)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    date_order = db.Column(db.DateTime)     #pick up date
    date_order_done= db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',back_populates='order')
    point=db.Column(db.String())

class Bonus(db.Model):
    __tablename__ = 'bonus'
    id = db.Column(db.Integer, primary_key=True)
    date_bonus = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User',back_populates='point_bonus')
    bonus=db.Column(db.Integer())
    voucher=db.Column(db.Integer())
