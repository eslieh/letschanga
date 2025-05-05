from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Configure naming convention for constraints
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

db = SQLAlchemy(metadata=metadata)

# Import models so they are registered with SQLAlchemy
from models.user import User
from models.notification import Notification
from models.user_info import UserInfo
from models.push_subscriptions import PushNotificationSubscription
from models.fundraiser import Fundraiser
from models.donation import Donation
from models.ledger import Transaction_ledger
from models.wallet  import Wallet