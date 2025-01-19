from http.client import HTTPException
from fastapi import status, logger
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import MembershipDetailCreateModel
from database.models import MembershipDetail
from auth.service import MemberService
from Gyms.service import GymService

gym_service=GymService()
member_service=MemberService()

class MembershipDetailService:
    async def add_detail_to_member(self,member_email:str,membershipdetail_data:MembershipDetailCreateModel,gym_uid:str,session:AsyncSession):
        try:
            gym=await gym_service.get_gym(gym_uid=gym_uid,session=session)
            member=await member_service.get_member_by_email(email=member_email,session=session)
            membership_detail_data_dict=membershipdetail_data.model_dump()
            new_membershipdetail=MembershipDetail(** membership_detail_data_dict)

            if not gym:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="Gym not found")
            if not member:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="Member not found")
            new_membershipdetail.member=member
            new_membershipdetail.gym=gym
            session.add(new_membershipdetail)
            await session.commit()
            return new_membershipdetail

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,details="Something went wrong")