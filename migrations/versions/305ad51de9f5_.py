"""empty message

Revision ID: 305ad51de9f5
Revises: 5de2f4216325
Create Date: 2019-01-23 15:27:33.824286

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '305ad51de9f5'
down_revision = '5de2f4216325'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('results')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('results',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('result_all', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.Column('result_no_stop_words', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='results_pkey')
    )
    # ### end Alembic commands ###
