import aioredis
from config import Config

from auth.utils import ACCESS_TOKEN_EXPIRY

JTI_EXPIRY=3600
token_bloklist=aioredis.StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT,db=0)

async def add_jti_to_blocklist(jti:str):
    await token_bloklist.set(name=jti,value="",ex=JTI_EXPIRY) # works as key value pair

async def token_in_blocklist(jti:str):
    jti=await token_bloklist.get(jti)
    return jti is not None