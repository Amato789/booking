"""delete image_id from hotels

Revision ID: 947c165595c4
Revises: a1d33748258f
Create Date: 2024-09-23 08:33:16.593421

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '947c165595c4'
down_revision: Union[str, None] = 'a1d33748258f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hotels', 'image_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotels', sa.Column('image_id', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
