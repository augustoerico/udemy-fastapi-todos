"""Create address table

Revision ID: c65a6fef15ce
Revises: e0a67483c76d
Create Date: 2023-02-23 14:13:05.372293

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c65a6fef15ce'
down_revision = 'e0a67483c76d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('addresses',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address1', sa.String(), nullable=False),
                    sa.Column('address2', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('contry', sa.String(), nullable=False),
                    sa.Column('postal_code', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('addresses')
