from flask import Flask
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_caching import Cache
from dotenv import load_dotenv
from flask_cors import CORS
from celery import Celery
import redis
import os
from models import db
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from datetime import timedelta
import threading


# import resources
from resources.auth_resource import SignupResource, VerifyOTPResource, LoginResource, ResendOTPResource, ForgotPasswordResource, ResetPasswordResource
from resources.my_fundraiser_resource import FundraiserListResource, FundraiserResource
from resources.user_resource import UserProfileResource
from resources.test_donate import TestDonations
from resources.upload_media_resource import ImageUploadResource
from resources.donate_resource import Donate_resource, Donatio_callBack
# Load environment variables from .efnv file
load_dotenv()

socketio = SocketIO()  # Declare at top-level
def create_app():
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)

    # Application configuration
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        RESEND_API_KEY=os.getenv("RESEND_API_KEY"),
        SQLALCHEMY_DATABASE_URI=os.getenv("CONNECTION_STRING"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key"),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=24),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        FRONTEND_URL=os.getenv("FRONTEND_URL", "http://localhost:3000"),

        # Caching config
        CACHE_TYPE="RedisCache",
        CACHE_REDIS_URL=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        CACHE_DEFAULT_TIMEOUT=300,
        PROFILE_CACHE_TTL=300,

        # Celery config
        CELERY_BROKER_URL=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        CELERY_RESULT_BACKEND=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        CELERY_TASK_SERIALIZER='json',
        CELERY_RESULT_SERIALIZER='json',
        CELERY_ACCEPT_CONTENT=['json'],
        CELERY_TIMEZONE='UTC',
        CELERY_ENABLE_UTC=True,

        # Web Push Notification Keys
        VAPID_PRIVATE_KEY=os.getenv("VAPID_PRIVATE_KEY"),
        VAPID_PUBLIC_KEY=os.getenv("VAPID_PUBLIC_KEY"),
        VAPID_CLAIMS=os.getenv("VAPID_CLAIMS")
    )

    # Initialize core extensions
    bcrypt = Bcrypt() 
    bcrypt.init_app(app)
    app.bcrypt = bcrypt
    # Password hashing
    db.init_app(app)                    # Database connection
    jwt = JWTManager(app)              # JWT authentication
    socketio.init_app(app, cors_allowed_origins="*")

    # Initialize caching and Redis
    cache = Cache(app)
    app.cache = cache
    app.redis = redis.Redis.from_url(app.config["CACHE_REDIS_URL"], decode_responses=True)

    # Lock to prevent race conditions (e.g. when creating categories)
    app.category_lock = threading.Lock()

    # Configure Celery for background tasks
    celery = Celery(app.import_name)
    celery.conf.update(app.config)
    app.celery = celery

    # Enable CORS for cross-origin requests
    CORS(app)

    # Database migrations setup
    migrate = Migrate(app, db)

    # Initialize OAuth (Google in this case)
    # oauth = OAuth(app)
    # google_oauth = GoogleOAuth(oauth, app.config['FRONTEND_URL'])

    # Initialize API and route definitions
    api = Api(app)

    # Custom task base class to allow Flask context in Celery tasks
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    # Health check endpoint for Redis
    class HealthCheck(Resource):
        def get(self):
            try:
                app.redis.ping()
                return {"status": "healthy", "redis": "connected"}, 200
            except redis.ConnectionError:
                return {"status": "healthy", "redis": "disconnected"}, 200

    # Register all API resources (routes)
    api.add_resource(HealthCheck, '/health')
        # Auth routes
    api.add_resource(SignupResource, '/auth/signup')
    api.add_resource(VerifyOTPResource, '/auth/verify-otp')
    api.add_resource(LoginResource, '/auth/login')
    api.add_resource(ResendOTPResource, '/auth/resend-otp')
    api.add_resource(ForgotPasswordResource, '/auth/forgot-password')
    api.add_resource(ResetPasswordResource, '/auth/reset-password')
    
       # userinfo
    api.add_resource(UserProfileResource, '/api/user/profile')
        
        # user fundraiser info
    api.add_resource(FundraiserListResource, "/api/my/fundraisers") #/api/fundraisers?page=1&limit=10
    api.add_resource(FundraiserResource, "/api/my/fundraisers/<string:fundraiser_id>")
    
    
    # donation resource
    #  Donate_resource, Donatio_callBack
    api.add_resource(Donate_resource, "/api/donate/mpesa")
    api.add_resource(Donatio_callBack, "/api/callback/mpesa/donation")
    # test donation and withdraw
    api.add_resource(TestDonations, '/api/test/donate')
    
    # upload media resource 
    api.add_resource(ImageUploadResource, '/api/media/upload')
    return app

# Run the app using Flask-SocketIO if this file is run directly
if __name__ == '__main__':
    app = create_app()
    socketio.run(
        app,
        host=os.getenv('HOST', '0.0.0.0'),
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('DEBUG', 'False').lower() == 'true'
    )
else:
    # For environments like WSGI servers
    app = create_app()
