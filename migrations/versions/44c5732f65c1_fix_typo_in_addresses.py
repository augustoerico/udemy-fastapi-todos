"""Fix typo in addresses

Revision ID: 44c5732f65c1
Revises: 229cf12a6566
Create Date: 2023-02-23 15:21:26.287181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44c5732f65c1'
down_revision = '229cf12a6566'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('addresses', 'contry', new_column_name='country')


def downgrade() -> None:
    pass
