"""AUTO: Added additional profile columns

Revision ID: 62405c51a954
Revises: 380f58b6172e
Create Date: 2025-03-06 18:43:47.768955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62405c51a954'
down_revision: Union[str, None] = '380f58b6172e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staff_profiles', sa.Column('muted_venue_ids', sa.ARRAY(sa.Integer()), server_default='{}', nullable=False))
    op.add_column('staff_profiles', sa.Column('hiatus', sa.Boolean(), server_default='false', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('staff_profiles', 'hiatus')
    op.drop_column('staff_profiles', 'muted_venue_ids')
    # ### end Alembic commands ###
