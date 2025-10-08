from flask import request,Blueprint,jsonify
from flask_jwt_extended import (get_jwt_identity,jwt_required,create_access_token,create_refresh_token)
from werkzeug.security import generate_password_hash,check_password_hash
from ..models import db, UserAccess

user_bp=Blueprint("user",__name__,url_prefix="/user/")

#registration 
@user_bp.route("/register",methods=["POST"])
def register():
        try:
            get_data=request.json
            name=get_data.get("name")
            email=get_data.get("email")
            password=get_data.get("password")
            role=get_data.get("role")
            
            check_proper_email=email.endswith("@gmail.com")
            if(check_proper_email):
                check_email=UserAccess.query.filter_by(email=email).first()
                if(not check_email):
                    pwd=generate_password_hash(password=password)
                    user=UserAccess(name=name,email=email,password=pwd,role=role)
                    db.session.add(user)
                    db.session.commit()
                    return {"Hurrah":f"{name} registration successfully"}
                else:
                    return {"Error Message":f"{name} your already registered"}
            else:
                return {'Error message':f"Hello {name}, Enter a valid email ending with @gmail.com"}
        except Exception as e:
            return jsonify({"error occured ": str(e)}), 500

    
#login
@user_bp.route("/login",methods=["GET"])
def login():
    try:
        get_data=request.json
        email=get_data.get("email")
        password=get_data.get("password")
        
        if(email.endswith("@gmail.com")):
            check_email=UserAccess.query.filter_by(email=email).first()
            if(check_email):
                check_pwd=check_password_hash(check_email.password,password)
                if(check_pwd):
                    access_token=create_access_token(identity=email)
                    refresh_token=create_refresh_token(identity=email)
                    return {
                        "Message":"Successfully Login",
                        "name":check_email.name,
                        "access_token":access_token,
                        'refresh_token':refresh_token
                    }
                else:
                    return {"Error Message":"Incorrect Password"}
            else:
                return {"Error Message":"Invalid user or Not registred"}
        else:
            return {"Error Message":"Email endswith @gmail.com"}
    except Exception as e:
        return {"Error occured":str(e)}
    

#get profile
@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    try:
        user_email = get_jwt_identity()
        get_user= UserAccess.query.filter_by(email=user_email).first()
        return jsonify({"username": get_user.name, "email": get_user.email})
    except Exception as e:
        return {"Error Ocurred":str(e)}

#refresh
@user_bp.route("/refresh_token",methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    try:
        get_token=get_jwt_identity()
        check_token=UserAccess.query.filter_by(email=get_token).first()
        if(check_token):
            new_token=create_access_token(identity=get_token)
            return {"New Access Token":new_token}
        else:
            return{"Error Message":"No User"}
    except Exception as e:
        return {"Error occured":str(e)}


# delete
@user_bp.route("/delete_user",methods=["DELETE"])
@jwt_required()
def delete_user():
    try:
        get_token=get_jwt_identity()
        check_user=UserAccess.query.filter_by(email=get_token).first()
        if(check_user):
            db.session.delete(check_user)
            db.session.commit()
            return {"Message":"Successfully deleted"}
        else:
            return {"Error Message":"No user"}
    except Exception as e:
        return {"Error occured":str(e)}
    

#modify_user_name
@user_bp.route("/modify_name",methods=["PUT"])
@jwt_required()
def change_user():
    try:
        new_name=request.json.get("name")
        get_token=get_jwt_identity()
        check_user=UserAccess.query.filter_by(email=get_token).first()
        if(check_user):
            check_user.name=new_name
            db.session.commit()
            return {"Message":"Successfully Change"}
        else:
            return {"Error Message":"No user"}
    except Exception as e:
        return {"Error occured":str(e)}
    
          

#change_password
@user_bp.route("/change_password",methods=["PUT"])
@jwt_required()
def change_password():
    try:
        get_token=get_jwt_identity()
        new_passowrd=request.json.get("password")
        user=UserAccess.query.filter_by(email=get_token).first()

        if(user):
            user.password=generate_password_hash(new_passowrd)
            db.session.commit()
            return "Password change successfully"
        else:
            return {"Error Message":"No user there"}
    except Exception as e:
        return {"Error":str(e)}
    