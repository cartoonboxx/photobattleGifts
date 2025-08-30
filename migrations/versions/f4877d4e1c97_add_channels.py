"""add channels

Revision ID: f4877d4e1c97
Revises: 6806780a70c7
Create Date: 2025-08-25 12:34:56.405809

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f4877d4e1c97'
down_revision: Union[str, Sequence[str], None] = '6806780a70c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: add channels column to prizes."""
    op.add_column(
        'prizes',
        sa.Column(
            'channels',
            postgresql.ARRAY(sa.Integer()),
            nullable=False,
            server_default='{}'
        )
    )


def downgrade() -> None:
    """Downgrade schema: remove channels column from prizes."""
    op.drop_column('prizes', 'channels')
