"""Create address_id to users table

Revision ID: 229cf12a6566
Revises: c65a6fef15ce
Create Date: 2023-02-23 14:35:27.368349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '229cf12a6566'
down_revision = 'c65a6fef15ce'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column(
        'address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('addresses_users_fk', source_table="users", referent_table="addresses", local_cols=[
                          'address_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('addresses_users_fk', table_name="users")
    op.drop_column('users', 'address_id')
