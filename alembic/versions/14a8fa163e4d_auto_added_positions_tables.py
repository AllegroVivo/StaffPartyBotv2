"""AUTO: Added positions tables

Revision ID: 14a8fa163e4d
Revises: 14ea9a71acd5
Create Date: 2025-02-22 08:32:55.677687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14a8fa163e4d'
down_revision: Union[str, None] = '14ea9a71acd5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('positions',
    sa.Column('top_level_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('role_id', sa.BigInteger(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['top_level_id'], ['top_level.id'], name='positions_top_level_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('requirements',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['position_id'], ['positions.id'], name='positions_requirements_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('top_level', sa.Column('temp_job_channel_id', sa.BigInteger(), nullable=True))
    op.add_column('top_level', sa.Column('profile_channel_id', sa.BigInteger(), nullable=True))
    op.add_column('top_level', sa.Column('welcome_channel_id', sa.BigInteger(), nullable=True))
    op.add_column('top_level', sa.Column('group_training_channel_id', sa.BigInteger(), nullable=True))
    op.add_column('top_level', sa.Column('restart_channel_ids', sa.ARRAY(sa.BigInteger()), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('top_level', 'restart_channel_ids')
    op.drop_column('top_level', 'group_training_channel_id')
    op.drop_column('top_level', 'welcome_channel_id')
    op.drop_column('top_level', 'profile_channel_id')
    op.drop_column('top_level', 'temp_job_channel_id')
    op.drop_table('requirements')
    op.drop_table('positions')
    # ### end Alembic commands ###
