from pyfcm import FCMNotification
import os
from models.push_subscriptions import PushNotificationSubscription
import logging
logger = logging.getLogger(__name__)

class SendPush:
    def __init__(self, user_id, message_title, message_body):
        self.user_id = user_id
        self.message_title = message_title
        self.message_body = message_body

    def send_push(self):
        # Initialize the FCM push service with your Firebase server key
        push_service = FCMNotification(server_key=os.getenv("FIREBASE_SERVER_KEY"))
        user_id = self.user_id
        # send push notification
        subs = PushNotificationSubscription.query.filter_by(user_id=user_id).all()
        if not subs:
            logger.info("user hasn't subscribed to notification")
        
        for sub in subs:
            device_token = sub.token
            # Send push to a single device
            # result = push_service.notify_single_device(
            #     registration_id=device_token,
            #     message_title=self.message_title,
            #     message_body=self.message_body
            # )

            # print("Push sent:", result)
            # return True
