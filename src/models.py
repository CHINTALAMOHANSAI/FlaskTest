from .extensions import db

class UserAccess(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))
    role=db.Column(db.String(50),default="user")

    def __repr__(self):
        return f"UserAcess {self.name}"
    
    def to_dict(self):
        return {"id":{self.id},"name":{self.name},"email":{self.email},"role":{self.role}}

    