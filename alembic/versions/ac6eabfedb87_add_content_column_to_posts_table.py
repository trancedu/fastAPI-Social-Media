"""add content column to posts table

Revision ID: ac6eabfedb87
Revises: acd58fe5a3cb
Create Date: 2023-02-28 14:33:10.196986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac6eabfedb87'
down_revision = 'acd58fe5a3cb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
