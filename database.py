from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)  # 更改此行
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    gender = db.Column(db.String(255), nullable=True)
    position = db.Column(db.String(255), nullable=True)


    def set_password(self, password):
        #self.password = generate_password_hash(password)
        self.password_hash = generate_password_hash(password)
        print(f"Generated password hash: {self.password_hash}")  # 添加此行

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    add_admin()

def add_admin():
    admin_username = '吕泽奥'
    admin = User.query.filter_by(username=admin_username).first()
    if not admin:
        admin = User(username=admin_username, gender='男', position='管理员', is_admin=True)
        admin.set_password('1008611')
        db.session.add(admin)
        db.session.commit()
    else:
        print(f"Admin user '{admin_username}' already exists.")


def change_password(self, new_password):
        self.password = new_password
        db.session.commit()

class PaymentContract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_time = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('payment_contracts', lazy=True))


class NonPaymentContract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cost_item_id = db.Column(db.Integer, db.ForeignKey('cost_item.id'), nullable=False)
    cost_item = db.relationship('CostItem', backref=db.backref('non_payment_contracts', lazy=True))
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('non_payment_contracts', lazy=True))


class CostItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cost_items', lazy=True))


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_time = db.Column(db.DateTime, nullable=False)
    payee = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('payments', lazy=True))


class CostAllocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cost_item_id = db.Column(db.Integer, db.ForeignKey('cost_item.id'), nullable=False)
    cost_item = db.relationship('CostItem', backref=db.backref('cost_allocations', lazy=True))
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    payment = db.relationship('Payment', backref=db.backref('cost_allocations', lazy=True))
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    allocation_date = db.Column(db.Date, nullable=False)  # 添加这一行

