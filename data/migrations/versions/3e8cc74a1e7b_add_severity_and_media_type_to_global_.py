"""Add severity and media_type to global messages

Revision ID: 3e8cc74a1e7b
Revises: fc47c1ec019f
Create Date: 2017-01-17 16:22:28.584237

"""

# revision identifiers, used by Alembic.
revision = "3e8cc74a1e7b"
down_revision = "fc47c1ec019f"

from alembic import op as original_op
from data.migrations.progress import ProgressWrapper
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade(tables, tester, progress_reporter):
    op = ProgressWrapper(original_op, progress_reporter)
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "messages", sa.Column("media_type_id", sa.Integer(), nullable=False, server_default="1")
    )
    op.add_column(
        "messages",
        sa.Column("severity", sa.String(length=255), nullable=False, server_default="info"),
    )
    op.alter_column(
        "messages",
        "uuid",
        existing_type=mysql.VARCHAR(length=36),
        server_default="",
        nullable=False,
    )
    op.create_index("messages_media_type_id", "messages", ["media_type_id"], unique=False)
    op.create_index("messages_severity", "messages", ["severity"], unique=False)
    op.create_index("messages_uuid", "messages", ["uuid"], unique=False)
    op.create_foreign_key(
        op.f("fk_messages_media_type_id_mediatype"),
        "messages",
        "mediatype",
        ["media_type_id"],
        ["id"],
    )
    # ### end Alembic commands ###

    op.bulk_insert(tables.mediatype, [{"name": "text/markdown"},])

    # ### population of test data ### #
    tester.populate_column("messages", "media_type_id", tester.TestDataType.Foreign("mediatype"))
    tester.populate_column("messages", "severity", lambda: "info")
    tester.populate_column("messages", "uuid", tester.TestDataType.UUID)
    # ### end population of test data ### #


def downgrade(tables, tester, progress_reporter):
    op = ProgressWrapper(original_op, progress_reporter)
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f("fk_messages_media_type_id_mediatype"), "messages", type_="foreignkey")
    op.drop_index("messages_uuid", table_name="messages")
    op.drop_index("messages_severity", table_name="messages")
    op.drop_index("messages_media_type_id", table_name="messages")
    op.alter_column("messages", "uuid", existing_type=mysql.VARCHAR(length=36), nullable=True)
    op.drop_column("messages", "severity")
    op.drop_column("messages", "media_type_id")
    # ### end Alembic commands ###

    op.execute(
        tables.mediatype.delete().where(
            tables.mediatype.c.name == op.inline_literal("text/markdown")
        )
    )
