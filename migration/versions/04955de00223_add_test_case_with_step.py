"""Add test case with step

Revision ID: 04955de00223
Revises: 32ee1261a8ca
Create Date: 2023-05-31 19:49:51.611443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04955de00223'
down_revision = '32ee1261a8ca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('test_case',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('precondition', sa.String(), nullable=True),
        sa.Column('postcondition', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['project.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_case_project_id'), 'test_case', ['project_id'], unique=False)
    op.create_table('test_step',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('test_case_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['test_case_id'], ['test_case.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_step_test_case_id'), 'test_step', ['test_case_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_test_step_test_case_id'), table_name='test_step')
    op.drop_table('test_step')
    op.drop_index(op.f('ix_test_case_project_id'), table_name='test_case')
    op.drop_table('test_case')
