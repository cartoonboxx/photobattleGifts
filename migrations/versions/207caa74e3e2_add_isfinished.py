"""add isFinished

Revision ID: 207caa74e3e2
Revises: 257f553cc22b
Create Date: 2025-08-22 15:26:37.267279
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '207caa74e3e2'
down_revision: Union[str, Sequence[str], None] = '257f553cc22b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавляем колонку с дефолтным значением False
    op.add_column(
        'prizes',
        sa.Column('isFinished', sa.Boolean(), nullable=False, server_default=sa.false())
    )
    # После заполнения всех существующих строк можно убрать server_default, если не нужен
    op.alter_column('prizes', 'isFinished', server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('prizes', 'isFinished')
