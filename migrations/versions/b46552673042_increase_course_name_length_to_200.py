"""Increase course name length to 200

Revision ID: b46552673042
Revises: 
Create Date: 2024-03-19 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b46552673042'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.alter_column('name',
                    existing_type=mysql.VARCHAR(length=80),
                    type_=sa.String(length=200),
                    existing_nullable=False)


def downgrade():
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.alter_column('name',
                    existing_type=sa.String(length=200),
                    type_=mysql.VARCHAR(length=80),
                    existing_nullable=False)
