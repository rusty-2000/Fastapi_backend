from http.client import HTTPException
from .service import MemberService
from fastapi.params import Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi import Request,status
from database.dbmain import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import decode_token
from fastapi.exceptions import HTTPException
from database.redis import token_bloklist, token_in_blocklist

member_service=MemberService()

class TokenBearer(HTTPBearer):
    def __init__(self,auto_error=True): # autoerror for behavior of class when error occurs
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request)->HTTPAuthorizationCredentials | None: # It allow us to access our credentials and create python object from class which act as function
        creds=await super().__call__(request)
        print(creds.scheme)
        print(creds.credentials)

        token = creds.credentials
        token_data=decode_token(token)
        if not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"error":"This token is Invalid or expired ","resolution":"Get the New Token"} )


        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"error":"This token is Invalid or revoked ","resolution":"Get the New Token"} )

        self.verify_token_data(token_data)
        return token_data

    def token_valid(self,token:str):
        token_data=decode_token(token)
        if token_data is not None:
            return True
        else:
            return False
    def verify_token_data(self,token_data):
        raise NotImplementedError("Please override this method in child classes ")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self,token_data:dict): # check if refresh token is sent to token that require access token
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Provide the access token")


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict):
        if token_data and not token_data['refresh']: # check if user is providing access token
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Provide the refresh token")

async def get_current_member(token_details:dict=Depends(AccessTokenBearer()),session:AsyncSession=Depends(get_session)):
    email=token_details['member']['email']
    member=await member_service.get_member_by_email(email,session)
    return member