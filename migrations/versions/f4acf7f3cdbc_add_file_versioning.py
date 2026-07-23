"""Add file versioning

Revision ID: f4acf7f3cdbc
Revises: 19eb1ae6e763
Create Date: 2026-07-22 14:42:16.598098
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = "f4acf7f3cdbc"
down_revision = "19eb1ae6e763"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("files") as batch_op:

        batch_op.add_column(
            sa.Column(
                "version",
                sa.Integer(),
                nullable=False,
                server_default="1"
            )
        )

        batch_op.add_column(
            sa.Column(
                "parent_file_id",
                sa.Integer(),
                nullable=True
            )
        )

        batch_op.create_foreign_key(
            "fk_files_parent_file_id",
            "files",
            ["parent_file_id"],
            ["id"]
        )


def downgrade():

    with op.batch_alter_table("files") as batch_op:

        batch_op.drop_constraint(
            "fk_files_parent_file_id",
            type_="foreignkey"
        )

        batch_op.drop_column("parent_file_id")

        batch_op.drop_column("version")