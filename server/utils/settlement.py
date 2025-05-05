from models.donation import Donation
from models.ledger import Transaction_ledger
from models.user import User
from models.push_subscriptions import PushNotificationSubscription
from models.fundraiser import Fundraiser
from models import db
from utils.send_push import SendPush
from utils.ledger_service import CreateLedger
import logging
logger = logging.getLogger(__name__)

class HandleSettlemt():
    def __init__(self, fundraiser_id, amount, transaction_ref):
        self.fundraiser_id = fundraiser_id
        self.amount = amount
        self.transaction_ref = transaction_ref
    
    def settle(self):
        fundraiser_id = self.fundraiser_id
        amount = self.amount
        transaction_ref=self.transaction_ref
        transaction_type="withdraw"
        status = "completed"
        
        fundraiser = Fundraiser.query.filter_by(fundraiser_id=fundraiser_id).first()
        if fundraiser:    
            # Update the fundraiser's current amount
            fundraiser.current_amount += amount
            db.session.commit()
            user_id=fundraiser.user_id     
            
            print("creating ledger")
            # create a ledger for that donation
            CreateLedger(transaction_ref, transaction_type, amount, fundraiser_id, status, user_id).ledge()
            # notify user on the new donatino
            message_title = "Fundraiser WithDraw"
            message_body = f"You've withdrawn Ksh {amount} just donated Ksh {amount}"     
              
            
            SendPush(user_id, message_title, message_body).send_push()
            
            