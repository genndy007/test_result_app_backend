"""Add test suite and run

Revision ID: bed7ee54ddc6
Revises: 04955de00223
Create Date: 2023-06-11 12:42:40.154484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bed7ee54ddc6'
down_revision = '04955de00223'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('test_suite',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['project.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_suite_project_id'), 'test_suite', ['project_id'], unique=False)
    op.create_table('test_case_test_suite',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('test_case_id', sa.Integer(), nullable=False),
        sa.Column('test_suite_id', sa.Integer(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['test_case_id'], ['test_case.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['test_suite_id'], ['test_suite.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_case_test_suite_test_case_id'), 'test_case_test_suite', ['test_case_id'], unique=False)
    op.create_index(op.f('ix_test_case_test_suite_test_suite_id'), 'test_case_test_suite', ['test_suite_id'], unique=False)
    op.create_table('test_run',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('test_suite_id', sa.Integer(), nullable=False),
        sa.Column('result', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['test_suite_id'], ['test_suite.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_run_test_suite_id'), 'test_run', ['test_suite_id'], unique=False)
    op.create_table('test_case_test_run',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('test_run_id', sa.Integer(), nullable=False),
        sa.Column('test_case_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['test_case_id'], ['test_case.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['test_run_id'], ['test_run.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_test_case_test_run_test_case_id'), 'test_case_test_run', ['test_case_id'], unique=False)
    op.create_index(op.f('ix_test_case_test_run_test_run_id'), 'test_case_test_run', ['test_run_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_test_case_test_run_test_run_id'), table_name='test_case_test_run')
    op.drop_index(op.f('ix_test_case_test_run_test_case_id'), table_name='test_case_test_run')
    op.drop_table('test_case_test_run')
    op.drop_index(op.f('ix_test_run_test_suite_id'), table_name='test_run')
    op.drop_table('test_run')
    op.drop_index(op.f('ix_test_case_test_suite_test_suite_id'), table_name='test_case_test_suite')
    op.drop_index(op.f('ix_test_case_test_suite_test_case_id'), table_name='test_case_test_suite')
    op.drop_table('test_case_test_suite')
    op.drop_index(op.f('ix_test_suite_project_id'), table_name='test_suite')
    op.drop_table('test_suite')
