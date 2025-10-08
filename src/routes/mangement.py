from flask import request, Blueprint,jsonify
from flask_jwt_extended import (get_jwt_identity, jwt_required)
from werkzeug.security import generate_password_hash
from ..models import db, UserAccess

manage_bp = Blueprint("management", __name__,url_prefix="/admin/")

#get_users
@manage_bp.route("/get_users",methods=["GET"])
@jwt_required()
def get_user():
    try:
        get_token = get_jwt_identity()
        check_user = UserAccess.query.filter_by(email=get_token).first()

        if (check_user.role == "admin"):
            users = UserAccess.query.all()
            # users=UserAccess.query.order_by(UserAccess.name.asc()).all()
            return {"all users": [{"id": i.id, "name": i.name, "email": i.email, "role": i.role} for i in users]}

        else:
            return {"Error Message": "Admin only access, User can't"}
    except Exception as e:
        return {"Error ocuured":str(e)}

#add_new_user
@manage_bp.route("/add_user",methods=["POST"])
@jwt_required()
def add_user():
    try:
        get_data=request.json
        name=get_data.get("name")
        email=get_data.get("email")
        password=get_data.get("password")
        role=get_data.get("role")

        get_token=get_jwt_identity()
        check_user=UserAccess.query.filter_by(email=get_token).first()

        if(not email.endswith("gmail.com")):
            return {"Error Message":"email ends with gmail.com"}
        
        if not check_user or check_user.role != "admin":
            return {"Error Message": "You are not admin you can't add users"}

        check_email=UserAccess.query.filter_by(email=email).first()
        if(not check_email):
            pwd=generate_password_hash(password=password)
            user=UserAccess(name=name,email=email,password=pwd,role=role)
            db.session.add(user)
            db.session.commit()
            return {"Message ":"Successfully created"}
        else:
            return {"Error Message":"Email already exist"}
        
    except Exception as e:
        return {"Error occured":str(e)}    

#get_by_id
@manage_bp.route("/get_by_id/<int:id>",methods=["GET"])
@jwt_required()
def get_by_id(id):
    try:
        get_token = get_jwt_identity()

        user_id=id 
        check_user = UserAccess.query.filter_by(email=get_token).first()
        if (check_user.role == "admin"):
            user = UserAccess.query.filter_by(id=user_id).first()
            if(user):
                return {"name":user.name,"email":user.email,"id":id}
            else:
                return {"Error Message":"No person having this id number"}
        else:
            return {"Error Message": "Admin only access, User can't"}
    except Exception as e:
        return {"Error occured":str(e)}
    
#delete_by_id
@manage_bp.route("/delete_by_id/<int:id>",methods=["DELETE"])
@jwt_required()
def delete_by_id(id):
    try:
        get_token = get_jwt_identity()
        user_id=id 
        check_user = UserAccess.query.filter_by(email=get_token).first()
        if (check_user.role == "admin"):
            user = UserAccess.query.filter_by(id=user_id).first()
            if(user):
                id=user.name
                db.session.delete(user)
                db.session.commit()
                return {"Message":f"{user.name} Deleted Successfully"}
            else:
                return {"Error Message":"No person having this id number"}
        else:
            return {"Error Message": "Admin only access, User can't"}
    except Exception as e:
        return {"Error occured":str(e)}
    



# @manage_bp.route("/reset_password",methods=["PUT"])
# @jwt_required()
# def reset_password():
#     try:
#         get_token=get_jwt_identity()
#         get_data=request.json 
#         email=get_data.get("email")
#         password=get_data.get("password")
#         check_user=UserAccess.query.filter_by(email=get_token).first()
        
#         if(check_user):
#             if(check_user.role=="admin"):
#                 check_user=UserAccess.query.filter_by(email=email).first()
#                 if(check_user):
#                     check_user.password=generate_password_hash(password=password)
#                     db.session.commit()
#                     return {"Message":"Succesfully reset the password"}
#                 else:
#                     return {"Error Message":"User is not there Invalid user"}
#             else:
#                 return {"Error Message":"Only Admin can"}
#         else:
#             return {"Message Error":"User is not there"}
#     except Exception as e:
#         return {"Error occured":str(e)}
    

