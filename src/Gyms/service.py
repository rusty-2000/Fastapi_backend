from sqlmodel.ext.asyncio.session  import AsyncSession
from .schemas import GymCreateModel, GymUpdateModel
from sqlmodel import select,desc
from database.models import Gym
from datetime import date, datetime
from sqlalchemy.orm import selectinload

class GymService:
    async def get_all_gyms(self,session:AsyncSession): # session is medium sqlalchemy or sqlmodel provide to access database and perform any operation
        statement= select(Gym).order_by(desc(Gym.created_at))
        result=await session.exec(statement)
        return result.all()

    async def get_member_gyms(self,member_uid:str,session:AsyncSession): # session is medium sqlalchemy or sqlmodel provide to access database and perform any operation
        statement= select(Gym).where(Gym.member_uid==member_uid).order_by(desc(Gym.created_at))
        result=await session.exec(statement)
        return result.all()

    async def get_gym(self, gym_uid: str, session: AsyncSession):
        print("1st line")
        #statement = select(Gym.membership_details).where(Gym.uid == gym_uid)
        statement = select(Gym).where(Gym.uid == gym_uid)
        print("2nd line")
        print(statement)
        result = await session.exec(statement)
        print("3rd line")
        gym = result.first()
        print("-------------")
        print(gym)
        return gym if gym else None

    async def create_gym(self,gym_data:GymCreateModel,member_uid:str,session:AsyncSession):
        """
        __edcwdc__:cdec
        :param gym_data:
        :param member_uid:
        :param session:
        :return:
        """
        gym_data_dict=gym_data.model_dump()
        new_gym=Gym(**gym_data_dict) # it will create new gym object with attributes it gets from this gym data dictionary
        new_gym.published_date=datetime.strptime(gym_data_dict['published_date'],"%Y-%m-%d")
        new_gym.member_uid=member_uid
        session.add(new_gym)
        await session.commit()
        return new_gym

    async def update_gym(self,gym_uid:str,update_data:GymUpdateModel, session:AsyncSession):
        gym_to_update=await self.get_gym(gym_uid,session)
        if gym_to_update is not None:
            update_data_dict=update_data.model_dump()
            for key,value in update_data_dict.items():
                setattr(gym_to_update,key,value) # get the object of gym_to_update and then update it
            await session.commit()
            return gym_to_update
        else:
            return None

    async def delete_a_gym(self,gym_uid:str,session:AsyncSession):
        gym_to_delete=await self.get_gym(gym_uid,session)
        if gym_to_delete is not None:
            await session.delete(gym_to_delete)
            await session.commit()
        else:
            return None