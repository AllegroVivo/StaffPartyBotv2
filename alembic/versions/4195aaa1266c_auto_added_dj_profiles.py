"""AUTO: added dj profiles

Revision ID: 4195aaa1266c
Revises: 806933a35121
Create Date: 2025-04-03 11:26:06.615865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4195aaa1266c'
down_revision: Union[str, None] = '806933a35121'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dj_profiles',
    sa.Column('top_level_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('color', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('nsfw', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('genres', sa.ARRAY(sa.Integer()), server_default='{}', nullable=False),
    sa.Column('aboutme', sa.String(), nullable=True),
    sa.Column('rates', sa.String(), nullable=True),
    sa.Column('logo_url', sa.String(), nullable=True),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('links', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
    sa.Column('dm_pref', sa.Boolean(), server_default='true', nullable=False),
    sa.ForeignKeyConstraint(['top_level_id'], ['top_level.id'], name='dj_profiles_top_level_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('dj_profile_availabilities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.BigInteger(), nullable=False),
    sa.Column('day', sa.Integer(), nullable=False),
    sa.Column('start_hour', sa.Integer(), nullable=False),
    sa.Column('start_minute', sa.Integer(), nullable=False),
    sa.Column('end_hour', sa.Integer(), nullable=False),
    sa.Column('end_minute', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['dj_profiles.user_id'], name='dj_profile_availability_dj_profiles_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dj_profile_availabilities')
    op.drop_table('dj_profiles')
    # ### end Alembic commands ###
