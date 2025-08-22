"""update type prizeSize

Revision ID: 257f553cc22b
Revises: 2699b644a62d
Create Date: 2025-08-22 14:58:40.014175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '257f553cc22b'
down_revision: Union[str, Sequence[str], None] = '2699b644a62d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.alter_column(
        'prizes',
        'prize_size',
        type_=sa.Integer(),
        existing_type=sa.VARCHAR(),
        postgresql_using="prize_size::integer"
    )

def downgrade():
    op.alter_column(
        'prizes',
        'prize_size',
        type_=sa.VARCHAR(),
        existing_type=sa.Integer(),
        postgresql_using="prize_size::text"
    )
