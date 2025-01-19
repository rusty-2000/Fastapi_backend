from datetime import datetime
from typing import List

from pydantic import BaseModel
import uuid
from datetime import datetime,date
from MembershipDetails.schemas import MembershipDetailModel

class GymCreateModel(BaseModel):
    gym_title:str
    owner:str
    published_date: str
    location: str
    language: str

class Gym(BaseModel):
    uid: uuid.UUID
    gym_title: str
    owner: str
    location: str
    published_date: date
    language: str
    created_at:datetime
    updated_at:datetime

class GymDetailModel(Gym):
    membership_details:List[MembershipDetailModel]

class GymUpdateModel(BaseModel):
    gym_title: str
    owner: str
    location: str
    language: str