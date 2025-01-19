import logging
from datetime import timedelta,datetime
from fastapi.responses import JSONResponse
from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException
from .service import MemberService
from .schemas import MemberCreateModel, MemberModel,MemberLoginModel,MemberGymsModel
from database.dbmain import get_session
from .utils import create_access_token,decode_token,verify_password
from .dependencies import RefreshTokenBearer, AccessTokenBearer,get_current_member
from database.redis import add_jti_to_blocklist

auth_router=APIRouter()
member_service=MemberService()
REFRESH_TOKEN_EXPIRY=1

@auth_router.post('/signup',response_model= MemberModel)
async def create_member_account(member_data:MemberCreateModel,session:AsyncSession=Depends(get_session)):
    logging.debug(f"Received member data: {member_data}")
    email=member_data.email
    member_exists=await member_service.member_exists(email,session)
    if member_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="member with email already exists")

    new_member=await member_service.create_member(member_data,session)
    return new_member

@auth_router.post('/login')
async def login_members(login_data:MemberLoginModel,session:AsyncSession=Depends(get_session)):
    email=login_data.email
    password=login_data.password
    member=await member_service.get_member_by_email(email,session)

    if member is not None:
        password_valid=verify_password(password,member.password_hash)
        if password_valid:
            access_token=create_access_token(member_data={'email':member.email,'member_uid':str(member.uid)})

            refresh_token=create_access_token(member_data={'email':member.email,'member_uid':str(member.uid)},refresh=True,expiry=timedelta(days=REFRESH_TOKEN_EXPIRY))
            return JSONResponse(content={"message":"Login Successfully","access_token":access_token,"refresh_token":refresh_token,"member":{"email":member.email,"uid":str(member.uid)}})

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Email or Password")

@auth_router.get('/refresh_token')
async def get_new_access_token(token_details:dict=Depends(RefreshTokenBearer())):
    expiry_timestamp=token_details['exp']
    if  datetime.fromtimestamp(expiry_timestamp) >datetime.now():
        new_access_token=create_access_token(member_data=token_details['member'])

        return JSONResponse(content={"access token":new_access_token})
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid or expired token")

@auth_router.get('/me',response_model=MemberGymsModel)
async def get_current_user(member=Depends(get_current_member)):
    return member

@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):
    jti=token_details['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(content={"message":"Logged out successfully"})