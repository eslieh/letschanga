from models.fundraiser import Fundraiser
from flask_socketio import SocketIO
socketio = SocketIO()
from models import db
from utils.send_push import SendPush
from utils.ledger_service import CreateLedger
import logging
import datetime
from flask import current_app
logger = logging.getLogger(__name__)

class HandleDonation():
    def __init__(self, fundraiser_id, amount, message, donor_name, transaction_ref):
        self.fundraiser_id = fundraiser_id
        self.amount = amount
        self.message = message
        self.donor_name = donor_name
        self.transaction_ref = transaction_ref
    
    def donate(self):
        fundraiser_id = self.fundraiser_id
        amount = self.amount
        message = self.message
        donor_name = self.donor_name
        transaction_ref=self.transaction_ref
        transaction_type="donation"
        
        fundraiser = Fundraiser.query.filter_by(fundraiser_id=fundraiser_id).first()
        if fundraiser:    
            # Update the fundraiser's current amount
            fundraiser.current_amount += amount
            db.session.commit()
            user_id=fundraiser.user_id     
            
            
            
        
            print("creating ledger")
            status = "completed"
            # create a ledger for that donation
            CreateLedger(transaction_ref, transaction_type, amount, fundraiser_id, status, user_id).ledge()
       
            # live update user
            cache = current_app
            target_sid = cache.get(f"user_sid:{user_id}")
            if target_sid:
                donation_payload = {
                    'donor_name': donor_name or 'Anonymous',
                    'amount': amount,
                    'message': message,
                    'timestamp': datetime.utcnow().isoformat()
                }
                socketio.emit('new_donation', donation_payload, room=target_sid)
            else:
                # notify user on the new donation, and the user is not online
                message_title = "New donatoin"
                message_body = f"{donor_name} just donated Ksh {amount}, {message}"     
                
                # SendPush(user_id, message_title, message_body).send_push()
            
            