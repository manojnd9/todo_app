"""add middle name to user

Revision ID: 4cd456a025da
Revises: e141ce029d31
Create Date: 2025-01-01 12:47:07.999739

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4cd456a025da"
down_revision: Union[str, None] = "e141ce029d31"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("middle_name", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "middle_name")
