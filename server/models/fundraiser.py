import uuid
from . import db
from sqlalchemy_serializer import SerializerMixin

class Fundraiser(db.Model, SerializerMixin):
    __tablename__ = 'fundraiser'
    id = db.Column(db.Integer, primary_key=True)
    fundraiser_id = db.Column(db.String(8), unique=True, default=lambda: str(uuid.uuid4()).split('-')[0])
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    goal_amount = db.Column(db.Float, nullable=False)
    current_amount = db.Column(db.Float, default=0.0)
    image_url = db.Column(db.String(255))
    deadline = db.Column(db.Date)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship("User", backref=db.backref("fundraisers", lazy=True))
