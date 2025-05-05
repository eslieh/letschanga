from . import db
from sqlalchemy_serializer import SerializerMixin

class PushNotificationSubscription(db.Model, SerializerMixin):
    __tablename__ = 'push_notification_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    subscription_id = db.Column(db.String(255), nullable=False)  # Unique subscription ID (web or mobile)
    device_type = db.Column(db.String(50), nullable=False)  # "web" or "mobile"
    endpoint = db.Column(db.String(255), nullable=True)  # URL endpoint for web push, null for mobile
    auth_token = db.Column(db.String(255), nullable=True)  # Auth token for web push
    p256dh = db.Column(db.String(255), nullable=True)  # Public key for web push
    is_active = db.Column(db.Boolean, default=True)  # Subscription status
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Timestamp when subscription was created
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())  # Timestamp for last update
