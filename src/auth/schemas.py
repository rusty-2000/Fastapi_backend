import uuid
from datetime import datetime, date
from typing import List
from pydantic import BaseModel
from sqlmodel import Field
from Gyms.schemas import Gym
class MemberCreateModel(BaseModel):
    member_name:str= Field(max_length=20)
    email:str= Field(max_length=20)
    password:str =Field(min_length=8)

class MemberModel(BaseModel):
    uid: uuid.UUID
    member_name: str
    email: str
    password_hash: str= Field(exclude=True)
    is_already_a_member: bool = Field(default=False)
    created_at: datetime
    updated_at: datetime

class MemberGymsModel(MemberModel):
    gyms: List[Gym]

class MemberLoginModel(BaseModel):
    email:str=Field(max_length=20)
    password:str=Field(min_length=8)