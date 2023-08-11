"""add content column

Revision ID: 8e6d8338ac7e
Revises: c6d2d505f0ff
Create Date: 2023-08-10 19:22:11.151882

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e6d8338ac7e'
down_revision: Union[str, None] = 'c6d2d505f0ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
