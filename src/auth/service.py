import logging
logging.basicConfig(level=logging.DEBUG)
from sqlmodel import select
from .schemas import MemberCreateModel
from database.models import Member
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import generate_passwd_hash


class MemberService:
    async def get_member_by_email(self,email:str,session:AsyncSession):
        statement=select(Member).where(Member.email==email)
        result= await session.exec(statement)
        member=result.first()
        return member

    async def member_exists(self,email:str,session:AsyncSession):
        member=await self.get_member_by_email(email,session)
        return True if member is not None else False

    async def create_member(self,member_data:MemberCreateModel,session:AsyncSession):
        member_data_dict=member_data.model_dump()
        logging.debug(f"Member data dictionary: {member_data_dict}")
        new_member=Member(**member_data_dict)
        new_member.password_hash=generate_passwd_hash(member_data_dict['password'])
        session.add(new_member)
        await session.commit()
        return new_member