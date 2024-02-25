"""many to one

Revision ID: 955eed7b540d
Revises: f724b8fb9b8c
Create Date: 2024-02-23 22:45:14.966859

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '955eed7b540d'
down_revision: Union[str, None] = 'f724b8fb9b8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('registered_on', sa.TIMESTAMP(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'registered_on')
    # ### end Alembic commands ###
