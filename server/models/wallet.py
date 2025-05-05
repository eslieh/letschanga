from sqlalchemy import Index
from sqlalchemy.orm import relationship
from datetime import datetime
from . import db

class Wallet(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0.0, nullable=False)  # Current balance in the wallet
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # When the wallet was created
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())  # When balance was last updated

    def deposit(self, amount):
        """Method to deposit funds into the wallet."""
        self.balance += amount
        db.session.commit()

    def withdraw(self, amount):
        """Method to withdraw funds from the wallet."""
        if self.balance >= amount:
            self.balance -= amount
            db.session.commit()
            return True
        return False

    def __repr__(self):
        return f'<Wallet {self.user_id} - Balance: {self.balance}>'
