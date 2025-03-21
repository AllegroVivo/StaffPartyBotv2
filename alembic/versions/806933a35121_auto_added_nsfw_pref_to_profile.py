"""AUTO: Added nsfw pref to profile

Revision ID: 806933a35121
Revises: ee6eac0df236
Create Date: 2025-03-17 15:36:21.425005

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '806933a35121'
down_revision: Union[str, None] = 'ee6eac0df236'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staff_profiles', sa.Column('nsfw_pref', sa.Boolean(), server_default='false', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('staff_profiles', 'nsfw_pref')
    # ### end Alembic commands ###
