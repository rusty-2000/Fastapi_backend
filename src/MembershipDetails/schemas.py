import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field

class MembershipDetailModel(BaseModel):
    uid: UUID
    rating: str
    type: str
    price: int
    gym_uid: Optional[uuid.UUID]
    member_uid: Optional[uuid.UUID]
    created_at:datetime
    updated_at:datetime


class MembershipDetailCreateModel(BaseModel):
    rating: str
    type: str
    price: int