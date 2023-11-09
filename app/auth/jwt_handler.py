# this file is responsible for sinning, encoding, decoding and returnin JWTs
import time 
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# function returns the generated tokens (JWTs)
def token_response(token: str):
    return {
        "acces token" : token 
    }

# function used for signign teh JWT string
def signJWT(userID : str):
    payload = {
        "userID" : userID,
        "empiry" : time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token : str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}