from fastapi import  APIRouter,Header, status , Depends,Path,Query
from .gym_data import Gyms
from .schemas import Gym, GymUpdateModel, GymCreateModel,GymDetailModel
from fastapi.exceptions import HTTPException
from typing import List
from database.dbmain import get_session
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from Gyms.service import GymService
from auth.dependencies import AccessTokenBearer

gym_router=APIRouter()
gym_service=GymService()
access_token_bearer=AccessTokenBearer()

@gym_router.get('/get_headers')
async def get_headers(accept:str=Header(None), content_type:str=Header(None), user_agent:str=Header(None),host:str=Header(None)):
    request_headers={}
    request_headers["Accept"]=accept
    request_headers["Content-Type"]=content_type
    request_headers["User_agent"]=user_agent
    request_headers["Host"]=host
    return request_headers


@gym_router.get("/home")
async def read_root():
    """
    this is the home fucntion for testing the fastapi,
    **testcase**:1
    *desc*: Testing the server
    __tags__: Home function
    _function_:async
    :return:
    """
    # hello
    return {"The base url link for /home path"}


@gym_router.get('/greet/',summary="welcome",response_description="aaiye apka sawagat hai")
#async def greet(name:str,age:Optional[int]=0)->dict:
#async def greet(name: str, age:int|None = 0) -> dict:
async def greet(name:str,age:int|None=Query(None,max_length=10,min_length=3)):
    return {"message": f"Hello {name}","age":age}

# @app.post('/create_gym')
# async def create_gym(gym_data:GymCreateModel):
#     return { "gym_title": gym_data.gym_title , "Gym_owner":gym_data.owner}

@gym_router.post('/',response_model=Gym,response_model_exclude_unset=True)
async def create_a_gym(gym_data:GymCreateModel,session:AsyncSession=Depends(get_session),token_detail=Depends(access_token_bearer)):
    member_id=token_detail.get('member')['member_uid']
    new_gym=await gym_service.create_gym(gym_data,member_id,session)
    return new_gym

@gym_router.get('/',response_model=List[Gym])
async def get_all_gyms(session:AsyncSession=Depends(get_session),token_detail=Depends(access_token_bearer)):
    gyms=await gym_service.get_all_gyms(session)
    return gyms

@gym_router.get('/member/{member_uid}',response_model=List[Gym])
async def get_member_gyms_subscryption(member_uid:str,session:AsyncSession=Depends(get_session),token_detail=Depends(access_token_bearer)):
    gyms=await gym_service.get_member_gyms(member_uid,session)
    return gyms

@gym_router.get('/{gym_id}',response_model=GymDetailModel)
async def get_a_gym(gym_uid:str=Path(...,alias="gym_id"),session: AsyncSession=Depends(get_session),token_detail=Depends(access_token_bearer)):
    gym=await gym_service.get_gym(gym_uid,session)
    if gym:
        return gym
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Gym Not Found")


@gym_router.patch('/{gym_uid}',response_model=Gym)
async def update_a_gym(gym_uid:str, gym_update_data:GymUpdateModel,session:AsyncSession=Depends(get_session),token_detail=Depends(access_token_bearer)):
    updated_gym=await gym_service.update_gym(gym_uid,gym_update_data,session)
    if updated_gym:
        return  updated_gym
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gym not found")

@gym_router.delete(("/{gym_uid}"))
async def delete_gym(gym_uid:str,session:AsyncSession=Depends(get_session),token_detail=Depends(access_token_bearer)):
    gym_to_delete= await gym_service.delete_a_gym(gym_uid,session)
    if gym_to_delete is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Gym not found")
    else:
        return "Successfully Deleted"