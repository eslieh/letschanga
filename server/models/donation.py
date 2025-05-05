from . import db
from sqlalchemy_serializer import SerializerMixin

class Donation(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    message = db.Column(db.String(255), nullable=True)
    fundraiser_id = db.Column(db.String(36), db.ForeignKey('fundraiser.fundraiser_id'), nullable=False)
    donor_name = db.Column(db.String(255), nullable=True, default="Anonymous")  # Default to "Anonymous"
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    donated = db.Column(db.Boolean, default=False, nullable=False)
    current_status = db.Column(db.String(255),default="initiated", nullable=True)
    merchant_request_id = db.Column(db.String(255), nullable=True)
    transaction_ref = db.Column(db.String(255), nullable=True)
    fundraiser = db.relationship('Fundraiser', backref='donations', lazy=True)
    