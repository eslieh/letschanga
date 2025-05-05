from sqlalchemy import Enum
import enum
from . import db
from sqlalchemy_serializer import SerializerMixin



# Enum to distinguish transaction types (Donation or Withdrawal)
class TransactionType(enum.Enum):
    DEBIT = "Donation"
    WITHDRAWAL = "Withdrawal"
    SERVICE  = "Service"
    REFUND = "Refund"

class Transaction_ledger(db.Model, SerializerMixin):
    __tablename__ = 'transaction_ledger'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_ref = db.Column(db.String(36), unique=True, nullable=False)  # Unique transaction reference
    transaction_type = db.Column(Enum(TransactionType), nullable=False)  # Type of the transaction (donation/withdrawal)
    amount = db.Column(db.Float, nullable=False)  # Amount of the transaction
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # User making the transaction
    fundraiser_id = db.Column(db.String(36), db.ForeignKey('fundraiser.fundraiser_id'), nullable=False)  # Related fundraiser
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Time of transaction
    status = db.Column(db.String(20), default="Pending")  # Transaction status (Pending, Completed, Failed)

    user = db.relationship('User', backref='transactions', lazy=True)
    fundraiser = db.relationship('Fundraiser', backref='transactions', lazy=True)
