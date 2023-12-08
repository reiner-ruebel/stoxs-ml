"""Users 3 fields

Revision ID: 80cb5233a81e
Revises: 7281fd45f425
Create Date: 2023-12-07 19:06:28.566759

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80cb5233a81e'
down_revision = '7281fd45f425'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('firstname', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('surname', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('title', sa.String(length=32), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('title')
        batch_op.drop_column('surname')
        batch_op.drop_column('firstname')

    # ### end Alembic commands ###