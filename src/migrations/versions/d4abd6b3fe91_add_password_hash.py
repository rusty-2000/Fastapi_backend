from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = 'd4abd6b3fe91'
down_revision: Union[str, None] = 'd990248843ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Get the current bind (connection)
    bind = op.get_bind()
    inspector = inspect(bind)

    # Check if 'password_hash' column exists
    if 'password_hash' not in [column['name'] for column in inspector.get_columns('members')]:
        op.add_column('members', sa.Column('password_hash', sqlmodel.sql.sqltypes.AutoString(), nullable=False))




def downgrade() -> None:
    # Add the 'password' column back
    op.add_column('members', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=False))

    # Drop the 'password_hash' column
    op.drop_column('members', 'password_hash')
