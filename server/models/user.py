from . import db
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Index


class User(db.Model, SerializerMixin):
    """User model representing application users."""
    __tablename__ = 'users'
    __table_args__ = (
        Index('idx_verification', 'otp_code', 'otp_expires_at'),
    )

    # Exclude sensitive fields and circular relationships
    serialize_rules = (
        '-password', '-otp_code', '-reset_token', '-reset_expires_at',
        '-conversations_as_giver', '-conversations_as_doer',
        '-messages_as_sender', '-messages_as_reciever',
        '-relations', '-related_to',
        '-tasks'
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(15), comment="Stored in E.164 format")
    image = db.Column(db.String(255), nullable=True, comment="URL to profile image")
    user_type = db.Column(db.String(255), nullable = False, default="user")
    otp_code = db.Column(db.String(6), nullable=True)
    otp_expires_at = db.Column(db.DateTime, nullable=True)
    otp_last_sent = db.Column(db.DateTime, nullable=True)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    reset_token = db.Column(db.String(64), nullable=True)
    reset_expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    status = db.Column(db.String(10), default="offline")  # 'online' or 'offline'
    last_seen = db.Column(db.DateTime, default=db.func.now())  # Last seen time

    def update_status(self, new_status):
        """Update user status and last seen time."""
        self.status = new_status
        if new_status == "offline":
            self.last_seen = db.func.now()
        db.session.commit()
