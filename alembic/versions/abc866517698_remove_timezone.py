"""remove timezone

Revision ID: abc866517698
Revises: 70fb4c14f45f
Create Date: 2024-09-10 07:31:27.618454

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'abc866517698'
down_revision: Union[str, None] = '70fb4c14f45f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('flashcard_reviews', 'date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=False)
    op.alter_column('flashcards', 'due_date',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True)
    op.alter_column('flashcards', 'created_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               type_=sa.DateTime(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('flashcards', 'created_at',
               existing_type=sa.DateTime(),
               type_=postgresql.TIMESTAMP(timezone=True),
               existing_nullable=True)
    op.alter_column('flashcards', 'due_date',
               existing_type=sa.DateTime(),
               type_=postgresql.TIMESTAMP(timezone=True),
               existing_nullable=True)
    op.alter_column('flashcard_reviews', 'date',
               existing_type=sa.DateTime(),
               type_=postgresql.TIMESTAMP(timezone=True),
               existing_nullable=False)
    # ### end Alembic commands ###
