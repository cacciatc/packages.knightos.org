"""add package file size

Revision ID: 2cc94456a9f
Revises: 2b1c28c108e
Create Date: 2016-07-29 10:25:41.969914

"""

# revision identifiers, used by Alembic.
revision = '2cc94456a9f'
down_revision = '2b1c28c108e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('package', sa.Column('file_size', sa.Integer(), nullable=True))

def downgrade():
    op.drop_column('package', 'file_size')
