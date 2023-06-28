"""updating videos table

Revision ID: 3b17f2b1f100
Revises: 
Create Date: 2023-06-18 18:42:50.525505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b17f2b1f100'
down_revision = None
branch_labels = None
depends_on = None

# alembic.ddl.base.add_column(compiler: DDLCompiler, column: Column[Any], **kw)

def upgrade():
    op.add_column('videos', sa.Column('title', sa.Text()))


def downgrade() -> None:
    pass
