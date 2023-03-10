"""auto-vote

Revision ID: 70759a5c3d59
Revises: b183b1c83d3c
Create Date: 2023-02-28 15:39:39.011450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70759a5c3d59'
down_revision = 'b183b1c83d3c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_table('votes')
    # ### end Alembic commands ###
