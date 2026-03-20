"""alter projects owner_id not null and add ondelete cascade

Revision ID: c3a4b5d6e7f8
Revises: 8d2593f3397a
Create Date: 2026-03-20 16:06:27.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c3a4b5d6e7f8"
down_revision: Union[str, Sequence[str], None] = "8d2593f3397a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the existing foreign key constraint
    op.drop_constraint("projects_owner_id_fkey", "projects", type_="foreignkey")

    # Make owner_id NOT NULL
    op.alter_column("projects", "owner_id", existing_type=sa.UUID(), nullable=False)

    # Recreate foreign key with ON DELETE CASCADE
    op.create_foreign_key(
        "projects_owner_id_fkey",
        "projects",
        "users",
        ["owner_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the CASCADE foreign key
    op.drop_constraint("projects_owner_id_fkey", "projects", type_="foreignkey")

    # Make owner_id nullable again
    op.alter_column("projects", "owner_id", existing_type=sa.UUID(), nullable=True)

    # Recreate original foreign key without CASCADE
    op.create_foreign_key(
        "projects_owner_id_fkey", "projects", "users", ["owner_id"], ["id"]
    )
