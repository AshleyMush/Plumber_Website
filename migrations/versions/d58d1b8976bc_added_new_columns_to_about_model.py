"""added new columns to about model

Revision ID: d58d1b8976bc
Revises: 
Create Date: 2025-01-08 07:39:02.114540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd58d1b8976bc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('AboutUsContent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('main_image_path', sa.String(length=2000), nullable=True))
        batch_op.add_column(sa.Column('image_one_path', sa.String(length=2000), nullable=True))
        batch_op.add_column(sa.Column('image_two_path', sa.String(length=2000), nullable=True))
        batch_op.add_column(sa.Column('content_one_url', sa.String(length=2000), nullable=True))
        batch_op.add_column(sa.Column('content_two_url', sa.String(length=2000), nullable=True))
        batch_op.add_column(sa.Column('content_three_url', sa.String(length=2000), nullable=True))
        batch_op.add_column(sa.Column('feature_one_heading', sa.String(length=2000), nullable=True))
        batch_op.add_column(sa.Column('feature_one_description', sa.String(length=2000), nullable=True))
        batch_op.add_column(sa.Column('feature_two_heading', sa.String(length=2000), nullable=True))
        batch_op.add_column(sa.Column('feature_two_description', sa.String(length=2000), nullable=True))
        batch_op.drop_column('image_one')
        batch_op.drop_column('image_two')
        batch_op.drop_column('content_url_one')
        batch_op.drop_column('description')
        batch_op.drop_column('content_url_two')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('AboutUsContent', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content_url_two', sa.VARCHAR(length=2000), nullable=True))
        batch_op.add_column(sa.Column('description', sa.VARCHAR(length=2000), nullable=True))
        batch_op.add_column(sa.Column('content_url_one', sa.VARCHAR(length=2000), nullable=True))
        batch_op.add_column(sa.Column('image_two', sa.VARCHAR(length=2000), nullable=True))
        batch_op.add_column(sa.Column('image_one', sa.VARCHAR(length=2000), nullable=True))
        batch_op.drop_column('feature_two_description')
        batch_op.drop_column('feature_two_heading')
        batch_op.drop_column('feature_one_description')
        batch_op.drop_column('feature_one_heading')
        batch_op.drop_column('content_three_url')
        batch_op.drop_column('content_two_url')
        batch_op.drop_column('content_one_url')
        batch_op.drop_column('image_two_path')
        batch_op.drop_column('image_one_path')
        batch_op.drop_column('main_image_path')

    # ### end Alembic commands ###
