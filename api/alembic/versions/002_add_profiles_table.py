"""Add profiles table

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create profiles table
    op.create_table(
        'profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('headline', sa.String(), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('skills', sa.JSON(), nullable=True),
        sa.Column('portfolio_links', sa.JSON(), nullable=True),
        sa.Column('availability', sa.String(), nullable=True),
        sa.Column('hourly_rate', sa.Float(), nullable=True),
        sa.Column('media_refs', sa.JSON(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('remote_preference', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('completeness_score', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_profiles_id'), 'profiles', ['id'], unique=False)
    op.create_index(op.f('ix_profiles_user_id'), 'profiles', ['user_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_profiles_user_id'), table_name='profiles')
    op.drop_index(op.f('ix_profiles_id'), table_name='profiles')
    op.drop_table('profiles')
