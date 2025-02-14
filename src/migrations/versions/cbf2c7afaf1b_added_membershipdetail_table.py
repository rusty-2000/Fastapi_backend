"""added membershipdetail table

Revision ID: cbf2c7afaf1b
Revises: 8ecdc075a962
Create Date: 2025-01-03 13:09:07.256432

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cbf2c7afaf1b'
down_revision: Union[str, None] = '8ecdc075a962'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('membership_details')
    # op.drop_table('members')
    # op.drop_table('gyms')
    # ### end Alembic commands ###


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###


    op.create_table('membership_details',
    sa.Column('uid', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('rating', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('gym_uid', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('member_uid', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['gym_uid'], ['gyms.uid'], name='membership_details_gym_uid_fkey'),
    sa.ForeignKeyConstraint(['member_uid'], ['members.uid'], name='membership_details_member_uid_fkey'),
    sa.PrimaryKeyConstraint('uid', name='membership_details_pkey')
    )
    # ### end Alembic commands ###
