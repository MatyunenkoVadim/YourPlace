"""Add column is_admin in users

Revision ID: 7c2038a287f5
Revises: f5463622f46d
Create Date: 2025-01-08 17:59:28.684152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Boolean, Column

# revision identifiers, used by Alembic.
revision: str = '7c2038a287f5'
down_revision: Union[str, None] = 'f5463622f46d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            Column(
                'is_admin',
                Boolean,
                nullable=False,
            ),
        )

def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column('is_admin')
