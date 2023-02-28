"""add foreign key to posts table

Revision ID: f49ac44f6315
Revises: bb76d6e5beed
Create Date: 2023-02-28 15:28:52.801155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f49ac44f6315'
down_revision = 'bb76d6e5beed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
