"""empty message

Revision ID: 9a1e90f9b29d
Revises: 9540d43c926f
Create Date: 2025-01-09 13:09:53.930099

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a1e90f9b29d'
down_revision: Union[str, None] = '9540d43c926f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('standards', sa.Column('correlation', sa.Float(), nullable=False))
    op.drop_column('standards', 'corelation')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('standards', sa.Column('corelation', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('standards', 'correlation')
    # ### end Alembic commands ###
