"""AUTO: Rebased db structure

Revision ID: 0562d02a655d
Revises: 
Create Date: 2025-03-10 15:35:23.571532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0562d02a655d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    top_level = op.create_table('top_level',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venue_channel_id', sa.BigInteger(), nullable=True),
    sa.Column('log_channel_id', sa.BigInteger(), nullable=True),
    sa.Column('temp_job_channel_id', sa.BigInteger(), nullable=True),
    sa.Column('perm_jobs_channel_id', sa.BigInteger(), nullable=True),
    sa.Column('profile_channel_id', sa.BigInteger(), nullable=True),
    sa.Column('welcome_channel_id', sa.BigInteger(), nullable=True),
    sa.Column('group_training_channel_id', sa.BigInteger(), nullable=True),
    sa.Column('bg_check_channel_id', sa.BigInteger(), nullable=True),
    sa.Column('restart_channel_ids', sa.ARRAY(sa.BigInteger()), nullable=True),
    sa.Column('staff_role_id', sa.BigInteger(), nullable=True),
    sa.Column('staff_pending_role_id', sa.BigInteger(), nullable=True),
    sa.Column('venue_management_role_id', sa.BigInteger(), nullable=True),
    sa.Column('trainee_role_id', sa.BigInteger(), nullable=True),
    sa.Column('trainee_hiatus_role_id', sa.BigInteger(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.bulk_insert(top_level, [{'id': 1}])
    op.create_table('guild_ids',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bg_checks',
    sa.Column('top_level_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('agree', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('names', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
    sa.Column('approved', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('post_url', sa.String(), nullable=True),
    sa.Column('submitted_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('approved_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('approved_by', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['top_level_id'], ['top_level.id'], name='bg_checks_top_level_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('permanent_jobs',
    sa.Column('top_level_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['top_level_id'], ['top_level.id'], name='permanent_jobs_top_level_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('staff_profiles',
    sa.Column('top_level_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('post_url', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('color', sa.Integer(), nullable=True),
    sa.Column('jobs', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
    sa.Column('rates', sa.String(), nullable=True),
    sa.Column('position_ids', sa.ARRAY(sa.Integer()), server_default='{}', nullable=False),
    sa.Column('dm_pref', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('timezone', sa.String(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('pronouns', sa.ARRAY(sa.Integer()), server_default='{}', nullable=False),
    sa.Column('race', sa.String(), nullable=True),
    sa.Column('clan', sa.String(), nullable=True),
    sa.Column('orientation', sa.String(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('age', sa.String(), nullable=True),
    sa.Column('mare', sa.String(), nullable=True),
    sa.Column('data_centers', sa.ARRAY(sa.Integer()), server_default='{}', nullable=False),
    sa.Column('likes', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
    sa.Column('dislikes', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
    sa.Column('personality', sa.String(), nullable=True),
    sa.Column('about_me', sa.String(), nullable=True),
    sa.Column('thumbnail_url', sa.String(), nullable=True),
    sa.Column('main_image_url', sa.String(), nullable=True),
    sa.Column('muted_venue_ids', sa.ARRAY(sa.Integer()), server_default='{}', nullable=False),
    sa.Column('hiatus', sa.Boolean(), server_default='false', nullable=False),
    sa.ForeignKeyConstraint(['top_level_id'], ['top_level.id'], name='bg_checks_top_level_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('venues',
    sa.Column('top_level_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('xiv_id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
    sa.Column('mare_id', sa.String(), nullable=True),
    sa.Column('mare_password', sa.String(), nullable=True),
    sa.Column('hiring', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('nsfw', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('data_center', sa.Integer(), nullable=True),
    sa.Column('world', sa.Integer(), nullable=True),
    sa.Column('zone', sa.Integer(), nullable=True),
    sa.Column('ward', sa.Integer(), nullable=True),
    sa.Column('plot', sa.Integer(), nullable=True),
    sa.Column('subdivision', sa.Boolean(), nullable=True),
    sa.Column('apartment', sa.Integer(), nullable=True),
    sa.Column('room', sa.Integer(), nullable=True),
    sa.Column('rp_level', sa.Integer(), nullable=True),
    sa.Column('tags', sa.ARRAY(sa.String()), server_default='{}', nullable=False),
    sa.Column('user_ids', sa.ARRAY(sa.BigInteger()), server_default='{}', nullable=False),
    sa.Column('position_ids', sa.ARRAY(sa.Integer()), server_default='{}', nullable=False),
    sa.Column('mute_ids', sa.ARRAY(sa.BigInteger()), server_default='{}', nullable=False),
    sa.Column('discord_url', sa.String(), nullable=True),
    sa.Column('website_url', sa.String(), nullable=True),
    sa.Column('banner_url', sa.String(), nullable=True),
    sa.Column('logo_url', sa.String(), nullable=True),
    sa.Column('app_url', sa.String(), nullable=True),
    sa.Column('post_url', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['top_level_id'], ['top_level.id'], name='venues_top_level_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bg_check_venues',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bg_check_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('data_center', sa.Integer(), nullable=False),
    sa.Column('world', sa.Integer(), nullable=False),
    sa.Column('jobs', sa.ARRAY(sa.String()), nullable=False),
    sa.ForeignKeyConstraint(['bg_check_id'], ['bg_checks.id'], name='bg_check_venues_bg_checks_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profile_additional_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.BigInteger(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('caption', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['staff_profiles.user_id'], name='profile_additional_images_profile_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profile_availabilities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.BigInteger(), nullable=False),
    sa.Column('day', sa.Integer(), nullable=False),
    sa.Column('start_hour', sa.Integer(), nullable=False),
    sa.Column('start_minute', sa.Integer(), nullable=False),
    sa.Column('end_hour', sa.Integer(), nullable=False),
    sa.Column('end_minute', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['staff_profiles.user_id'], name='profile_availability_profile_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('temporary_jobs',
    sa.Column('top_level_id', sa.Integer(), server_default='1', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('candidate_id', sa.BigInteger(), nullable=True),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('position_id', sa.Integer(), nullable=False),
    sa.Column('post_url', sa.String(), nullable=True),
    sa.Column('salary', sa.String(), nullable=True),
    sa.Column('start_dt', sa.TIMESTAMP(), nullable=False),
    sa.Column('end_dt', sa.TIMESTAMP(), nullable=False),
    sa.ForeignKeyConstraint(['top_level_id'], ['top_level.id'], name='temporary_jobs_top_level_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], name='temporary_jobs_venues_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venue_schedules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('day', sa.Integer(), nullable=True),
    sa.Column('start_hour', sa.Integer(), nullable=True),
    sa.Column('start_minute', sa.Integer(), nullable=True),
    sa.Column('end_hour', sa.Integer(), nullable=True),
    sa.Column('end_minute', sa.Integer(), nullable=True),
    sa.Column('interval_type', sa.Integer(), nullable=True),
    sa.Column('interval_arg', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], name='venue_schedules_venues_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venue_schedules')
    op.drop_table('temporary_jobs')
    op.drop_table('profile_availabilities')
    op.drop_table('profile_additional_images')
    op.drop_table('bg_check_venues')
    op.drop_table('venues')
    op.drop_table('staff_profiles')
    op.drop_table('permanent_jobs')
    op.drop_table('bg_checks')
    op.drop_table('top_level')
    op.drop_table('guild_ids')
    # ### end Alembic commands ###
