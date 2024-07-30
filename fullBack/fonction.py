from django.db import models
from django.db import connection
import mysql.connector
from django.conf import settings

def Query(query, params=None):
    conn = mysql.connector.connect(
        host=settings.DATABASES['default']['HOST'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        database=settings.DATABASES['default']['NAME'],
        port=settings.DATABASES['default']['PORT']
    )
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result

def get_user_id(email, password):
    query = "SELECT id_user FROM User WHERE email = %s AND password = %s"
    params = (email, password)
    row = Query(query, params)
    
    if row:
        return row[0][0]
    else:
        return None

def get_user_name(email, password):
    query = "SELECT name FROM User WHERE email = %s AND password = %s"
    params = (email, password)
    row = Query(query, params)
    
    if row:
        return row[0][0]
    else:
        return None

def get_all_info_user(email,password):
    query = "SELECT id_user,email,name,telephone FROM User WHERE email = %s AND password = %s"
    params = (email, password)
    array = Query(query, params)
    
    if array:
        return array[0]
    else:
        return None


import jwt
from datetime import datetime, timedelta

def generate_token(email, password):
    user_id = get_user_id(email, password)
    name = get_user_name(email, password)
    user = get_all_info_user(email, password)
    # query = Query("SELECT * FROM `User` WHERE id_user = %s", {user_id,})
    payload = {
        'user_id': user_id,
        'email':email,
        'name':name,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    
    return {"_token":token, "user":user}