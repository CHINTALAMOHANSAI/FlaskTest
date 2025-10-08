from datetime import timedelta
class Config:
    SQLALCHEMY_DATABASE_URI="sqlite:///demo.db"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY="dev" 
    JWT_SECRET_KEY="secret_dev"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=10)
