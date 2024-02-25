"""check user

Revision ID: 14e60d763520
Revises: c88d0b09fdf2
Create Date: 2024-02-23 20:45:34.877394

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '14e60d763520'
down_revision: Union[str, None] = 'c88d0b09fdf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('api_key_user_id_fkey', 'api_key', type_='foreignkey')
    op.drop_column('api_key', 'key_name')
    op.drop_column('api_key', 'hashed_key')
    op.drop_column('api_key', 'user_id')
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(length=1024),
               nullable=False)
    op.drop_column('user', 'registered_on')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('registered_on', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(length=1024),
               nullable=True)
    op.add_column('api_key', sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=True))
    op.add_column('api_key', sa.Column('hashed_key', sa.VARCHAR(length=1024), autoincrement=False, nullable=True))
    op.add_column('api_key', sa.Column('key_name', sa.VARCHAR(length=55), autoincrement=False, nullable=False))
    op.create_foreign_key('api_key_user_id_fkey', 'api_key', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###