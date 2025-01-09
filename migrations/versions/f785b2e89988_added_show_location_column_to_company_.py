from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f785b2e89988'
down_revision = 'd58d1b8976bc'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('CompanyDetails', schema=None) as batch_op:
        batch_op.add_column(sa.Column('show_location', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))

def downgrade():
    with op.batch_alter_table('CompanyDetails', schema=None) as batch_op:
        batch_op.drop_column('show_location')