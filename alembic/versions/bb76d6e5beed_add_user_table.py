"""add user table

Revision ID: bb76d6e5beed
Revises: ac6eabfedb87
Create Date: 2023-02-28 14:36:40.604056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb76d6e5beed'
down_revision = 'ac6eabfedb87'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email' )
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
