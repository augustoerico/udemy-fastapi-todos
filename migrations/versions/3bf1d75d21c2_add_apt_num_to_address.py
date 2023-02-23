"""Add apt_num to address

Revision ID: 3bf1d75d21c2
Revises: 44c5732f65c1
Create Date: 2023-02-23 15:51:08.786995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bf1d75d21c2'
down_revision = '44c5732f65c1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('addresses', sa.Column('apt_num', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('addresses', 'apt_num')
