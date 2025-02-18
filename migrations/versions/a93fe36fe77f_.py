"""empty message

Revision ID: a93fe36fe77f
Revises: 79f1432d8b7b
Create Date: 2024-12-07 14:57:59.110783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a93fe36fe77f'
down_revision = '79f1432d8b7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clausules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clausules')
    # ### end Alembic commands ###
