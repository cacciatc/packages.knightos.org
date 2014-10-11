"""Add 'approved' to packages

Revision ID: 2c9bcf7f568
Revises: 2ca4511880b
Create Date: 2014-10-11 16:54:28.384676

"""

# revision identifiers, used by Alembic.
revision = '2c9bcf7f568'
down_revision = '2ca4511880b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('package', sa.Column('approved', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('package', 'approved')
    ### end Alembic commands ###
