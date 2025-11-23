"""Create embeds table

Revision ID: c0632533e8d0
Revises:
Create Date: 2025-11-23 14:03:43.657542

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c0632533e8d0"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "embeds",
        sa.Column("id", sa.VARCHAR(), primary_key=True),
        sa.Column("created_at", sa.BIGINT(), server_default=sa.func.now()),
        sa.Column("title", sa.VARCHAR()),
        sa.Column("author", sa.VARCHAR()),
        sa.Column("description", sa.VARCHAR()),
        sa.Column("image", sa.VARCHAR()),
        sa.Column("is_image_thumbnail", sa.BOOLEAN(), nullable=False),
        sa.Column("color", sa.VARCHAR()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("embeds")
