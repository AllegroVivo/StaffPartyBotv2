"""AUTO: added training_ids and bg_check_done to Profiles

Revision ID: 4391d055b854
Revises: 9d3d6a9ecd8f
Create Date: 2025-03-13 15:37:44.854309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4391d055b854'
down_revision: Union[str, None] = '9d3d6a9ecd8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staff_profiles', sa.Column('training_ids', sa.ARRAY(sa.Integer()), server_default='{}', nullable=False))
    op.add_column('staff_profiles', sa.Column('bg_check_done', sa.Boolean(), server_default='false', nullable=False))
    op.drop_column('staff_profiles', 'hiatus')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staff_profiles', sa.Column('hiatus', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.drop_column('staff_profiles', 'bg_check_done')
    op.drop_column('staff_profiles', 'training_ids')
    # ### end Alembic commands ###
