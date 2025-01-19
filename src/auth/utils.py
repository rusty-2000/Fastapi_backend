# for utility funciton that shall use as far as authentication is concerned
import logging
from datetime import timedelta, datetime
import jwt
from config import Config
from passlib.context import CryptContext
import uuid
passwd_context=CryptContext(schemes=['bcrypt'])
ACCESS_TOKEN_EXPIRY=3600

def generate_passwd_hash(password:str):
    hash=passwd_context.hash(password)
    return hash

def verify_password(password:str,hash:str) -> bool:
    return passwd_context.verify(password,hash)

def create_access_token(member_data:dict,expiry:timedelta=None,refresh:bool=False):
    payload={}
    payload['member']=member_data
    payload['exp']=datetime.now()+ (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti']=str(uuid.uuid4)
    payload['refresh']=refresh

    token=jwt.encode(payload=payload,key=Config.JWT_SECRET,algorithm=Config.JWT_ALGORITHM)
    return token

def decode_token(token:str):
    try:
        token_data=jwt.decode(jwt=token,key=Config.JWT_SECRET,algorithms=[Config.JWT_ALGORITHM])
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None