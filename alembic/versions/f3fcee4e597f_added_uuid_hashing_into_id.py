"""added uuid hashing into id

Revision ID: f3fcee4e597f
Revises: 2beec5fe5408
Create Date: 2026-09-09 18:41:28.974198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3fcee4e597f'
down_revision: Union[str, Sequence[str], None] = '2beec5fe5408'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint('table_products_user_id_fkey', 'table_products', type_='foreignkey')

    op.alter_column('table_users', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False,
               postgresql_using='id::varchar')

    op.alter_column('table_products', 'user_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True, # или False, в зависимости от твоей модели
               postgresql_using='user_id::varchar')
    op.alter_column('table_products', 'id',
                    existing_type=sa.INTEGER(),
                    type_=sa.String(),
                    existing_nullable=True,  # или False, в зависимости от твоей модели
                    postgresql_using='user_id::varchar')

    op.create_foreign_key('table_products_user_id_fkey', 'table_products', 'table_users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('table_products_user_id_fkey', 'table_products', type_='foreignkey')

    op.alter_column('table_products', 'user_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               postgresql_using='user_id::integer')

    op.alter_column('table_users', 'id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               postgresql_using='id::integer')

    op.create_foreign_key('table_products_user_id_fkey', 'table_products', 'table_users', ['user_id'], ['id'])