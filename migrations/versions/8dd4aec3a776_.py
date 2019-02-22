"""empty message

Revision ID: 8dd4aec3a776
Revises: 1c02764cb65f
Create Date: 2019-02-20 18:19:17.082705

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8dd4aec3a776'
down_revision = '1c02764cb65f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('classes', sa.Column('hours', sa.Integer(), nullable=True))
    op.add_column('classes', sa.Column('type', sa.String(), nullable=True))
    op.drop_column('classes', 'year')
    op.drop_column('classes', 'teachers')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('classes', sa.Column('teachers', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.add_column('classes', sa.Column('year', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('classes', 'type')
    op.drop_column('classes', 'hours')
    # ### end Alembic commands ###