"""add qty

Revision ID: 5f915c0a4158
Revises: 25d326e18dc9
Create Date: 2024-09-02 16:12:56.909091

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f915c0a4158'
down_revision: Union[str, None] = '25d326e18dc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('items', sa.Column('qty', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_items_qty'), 'items', ['qty'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_items_qty'), table_name='items')
    op.drop_column('items', 'qty')
    # ### end Alembic commands ###
