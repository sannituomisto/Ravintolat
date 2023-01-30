import os
from database import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    sql = text("SELECT id, password, is_admin FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if not check_password_hash(hash_value, password):
            return False
        session["user_id"] = user[1]
        session["user_name"] = username
        session["user_is_admin"] = user[2]
        session["csrf_token"] = os.urandom(16).hex()
        return True

def register(username,password,is_admin):
    hash_value = generate_password_hash(password)
    try:
        sql = text("""INSERT INTO users (username, password, is_admin) VALUES (:username, :password, :is_admin)""")
        db.session.execute(sql, {"username":username, "password":hash_value, "is_admin":is_admin})
        db.session.commit()
    except:
        return False

    return login(username, password)


def get_user(username):
    sql=text("SELECT id, username, is_admin FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user


    

    
