import jwt 
from functools import wraps
from flask import request, jsonify
from var_env import VAR_ENV
from .models import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'authorization' in request.headers:
            token = request.headers['authorization']
        
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        
        try:
            data = jwt.decode(token, VAR_ENV['JWT_SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        return  f(*args, **kwargs)
  
    return decorated