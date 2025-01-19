from typing import Optional, List
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import SQLModel, Field, Column, Relationship
import uuid
from datetime import datetime, date
from uuid import UUID


class Member(SQLModel, table=True):
    __tablename__ = 'members'
    uid: UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    member_name: str
    email: str
    password_hash: str = Field(exclude=True)  # exclude tells whether field should be serialized using this model
    is_already_a_member: bool = Field(default=False)
    gyms: List["Gym"] = Relationship(back_populates="member", sa_relationship_kwargs={"lazy": "selectin"})
    membership_details: List["MembershipDetail"] = Relationship(back_populates="member", sa_relationship_kwargs={"lazy": "selectin"})
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<Member {self.member_name}>"


class Gym(SQLModel, table=True):
    __tablename__ = "gyms"
    uid: UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    gym_title: str
    owner: str
    location: str
    published_date: date
    language: str
    member_uid: Optional[UUID] = Field(default=None, foreign_key="members.uid")
    membership_details: List["MembershipDetail"] = Relationship(back_populates="gym" , sa_relationship_kwargs={"lazy": "selectin"})
    member: Optional["Member"] = Relationship(back_populates="gyms")  # all gym related to the member
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<Gym {self.gym_title}>"


class MembershipDetail(SQLModel, table=True):
    __tablename__ = "membership_details"
    uid: UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    rating: str
    type: str
    price: int
    gym_uid: Optional[UUID] = Field(default=None, foreign_key="gyms.uid")
    member_uid: Optional[UUID] = Field(default=None, foreign_key="members.uid")
    member: Optional["Member"] = Relationship(back_populates="membership_details")  # membership details linked to a member
    gym: Optional["Gym"] = Relationship(back_populates="membership_details")  # membership details linked to a gym
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<Membership of {self.gym_uid} by {self.member_uid}>"