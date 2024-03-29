"""change_currency_table

Revision ID: 65782d6d73e3
Revises: 1c7eb0f4abd6
Create Date: 2024-02-20 19:56:25.100494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65782d6d73e3'
down_revision = '1c7eb0f4abd6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('currency', 'code',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('currency', 'rate',
               existing_type=sa.NUMERIC(precision=100, scale=0),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('currency', 'rate',
               existing_type=sa.NUMERIC(precision=100, scale=0),
               nullable=False)
    op.alter_column('currency', 'code',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
