from app import db
from datetime import datetime

class Client(db.Model):
    """Модель клиента"""
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    client_code = db.Column(db.Integer, unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Обычный клиент')
    age = db.Column(db.Integer)
    city = db.Column(db.String(50))
    avg_monthly_balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    transactions = db.relationship('Transaction', backref='client', lazy='dynamic')
    transfers = db.relationship('Transfer', backref='client', lazy='dynamic')
    product_benefits = db.relationship('ProductBenefit', backref='client', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_code': self.client_code,
            'name': self.name,
            'status': self.status,
            'age': self.age,
            'city': self.city,
            'avg_monthly_balance': self.avg_monthly_balance,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Transaction(db.Model):
    """Модель транзакции"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    client_code = db.Column(db.Integer, db.ForeignKey('clients.client_code'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='KZT')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_code': self.client_code,
            'date': self.date.isoformat() if self.date else None,
            'category': self.category,
            'amount': self.amount,
            'currency': self.currency,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Transfer(db.Model):
    """Модель перевода"""
    __tablename__ = 'transfers'
    
    id = db.Column(db.Integer, primary_key=True)
    client_code = db.Column(db.Integer, db.ForeignKey('clients.client_code'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String(50), nullable=False)  # salary_in, salary_out, deposit, withdrawal, etc.
    direction = db.Column(db.String(10), nullable=False)  # in, out
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='KZT')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_code': self.client_code,
            'date': self.date.isoformat() if self.date else None,
            'type': self.type,
            'direction': self.direction,
            'amount': self.amount,
            'currency': self.currency,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ProductBenefit(db.Model):
    """Модель расчета выгоды по продуктам"""
    __tablename__ = 'product_benefits'
    
    id = db.Column(db.Integer, primary_key=True)
    client_code = db.Column(db.Integer, db.ForeignKey('clients.client_code'), nullable=False, index=True)
    product = db.Column(db.String(100), nullable=False)
    expected_benefit = db.Column(db.Float, default=0.0)
    push_notification = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_code': self.client_code,
            'product': self.product,
            'expected_benefit': self.expected_benefit,
            'push_notification': self.push_notification,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
