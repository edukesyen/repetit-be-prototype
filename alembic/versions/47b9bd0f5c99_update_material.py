"""update material

Revision ID: 47b9bd0f5c99
Revises: 0e0b4f0cc223
Create Date: 2024-09-09 14:56:55.796257

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '47b9bd0f5c99'
down_revision: Union[str, None] = '0e0b4f0cc223'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('materials', sa.Column('name', sa.String(), nullable=False))
    op.drop_column('materials', 'type')
    op.drop_column('materials', 'file_name')
    op.drop_column('materials', 'file_path')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('materials', sa.Column('file_path', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('materials', sa.Column('file_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('materials', sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('materials', 'name')
    # ### end Alembic commands ###
