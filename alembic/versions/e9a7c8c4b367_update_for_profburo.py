"""update for profburo

Revision ID: e9a7c8c4b367
Revises: d26d321737ae
Create Date: 2024-09-16 14:09:46.585441

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e9a7c8c4b367"
down_revision: Union[str, None] = "d26d321737ae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "ProfburoMembers", "info", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "ProfburoMembers", "direction", existing_type=sa.VARCHAR(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "ProfburoMembers", "direction", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "ProfburoMembers", "info", existing_type=sa.VARCHAR(), nullable=False
    )
    # ### end Alembic commands ###
