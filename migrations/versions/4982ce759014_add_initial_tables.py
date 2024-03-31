"""add: initial tables

Revision ID: 4982ce759014
Revises: 
Create Date: 2024-03-07 01:31:36.240357

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4982ce759014'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(sa.text("""
    create or replace function generate_compost_id(
    id_entity integer,
    "type" varchar,
    cost numeric
    ) RETURNS VARCHAR AS $$
        begin
            return cast(id_entity as varchar) || '-' || "type" || '-' || replace(cast(cost as varchar), ',', '-'); 
        end;
        $$ language plpgsql immutable
    """))

    op.create_table('entity',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    schema='financial'
    )
    op.create_table('acc_payable',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_entity', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=10), nullable=False),
    sa.Column('cost', sa.Numeric(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text("now()")),
    sa.Column('status', sa.Boolean(), nullable=False, server_default=sa.text("true")),
    sa.Column("compost_id", sa.String(30), unique=True, nullable=False, server_default=sa.Computed("generate_compost_id(id_entity, type, cost)")),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('compost_id'),
    sa.ForeignKeyConstraint(['id_entity'], ['financial.entity.id']),
    schema='financial'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entity', schema='financial')
    op.drop_table('acc_payable', schema='financial')
    # ### end Alembic commands ###
