from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .service import MembershipDetailService
from MembershipDetails.schemas import MembershipDetailCreateModel
from database.dbmain import get_session
from database.models import Member
from auth.routes import member_service
from auth.dependencies import get_current_member
membershipdetail_service=MembershipDetailService()

membership_router=APIRouter()

@membership_router.post('/gym/{gym_uid}')
async def add_membership_detail_to_gyms(gym_uid:str,membership_detail_data:MembershipDetailCreateModel,current_member:Member=Depends(get_current_member),session:AsyncSession=Depends(get_session)):
    new_membership_detail=await membershipdetail_service.add_detail_to_member(member_email=current_member.email,membershipdetail_data=membership_detail_data,gym_uid=gym_uid,session=session)
    return new_membership_detail