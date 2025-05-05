from models.ledger import Transaction_ledger
from models import db
import uuid
import logging
class CreateLedger():
    def __init__(self, transaction_ref, transaction_type, amount, fundraiser_id, status, user_id=False):
        self.transaction_ref = transaction_ref
        self.transaction_type = transaction_type
        self.amount = amount
        self.fundraiser_id = fundraiser_id
        self.status = status
        self.user_id = user_id
    def ledge(self):
        ledger_entry = Transaction_ledger(
            transaction_ref=self.transaction_ref,
            transaction_type= "DONATION" if self.transaction_type == "donation" else "WITHDRAWAL",
            amount=self.amount,
            fundraiser_id=self.fundraiser_id,
            user_id=self.user_id,
            status=self.status
        )
        db.session.add(ledger_entry)
        db.session.commit()
        print("success, legger created sucessfully")
        