"""empty message

Revision ID: 38309123ccfc
Revises: 
Create Date: 2025-03-12 01:19:38.000972

"""

from alembic import op
import sqlalchemy as sa
from fastapi_storages.integrations.sqlalchemy import ImageType


# revision identifiers, used by Alembic.
revision = '38309123ccfc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'transactions',
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('amount', sa.Numeric(), nullable=False),
        sa.Column('transaction_type', sa.Enum('WITHDRAW', 'DEPOSIT', name='transactiontype'), nullable=False),
        sa.Column(
            'status', sa.Enum('PENDING', 'SUCCESS', 'CANCELLED', 'ERROR', name='transactionstatus'), nullable=False
        ),
        sa.Column('payment_redirect', sa.String(), nullable=False),
        sa.Column('confirmation_url', sa.String(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_transactions')),
    )
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=True)
    op.create_table(
        'user_balances',
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('balance', sa.String(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_user_balances')),
    )
    op.create_index(op.f('ix_user_balances_id'), 'user_balances', ['id'], unique=True)
    op.create_table(
        'user_payment_info',
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('rebill_id', sa.String(), nullable=False),
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_user_payment_info')),
    )
    op.create_index(op.f('ix_user_payment_info_id'), 'user_payment_info', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_payment_info_id'), table_name='user_payment_info')
    op.drop_table('user_payment_info')
    op.drop_index(op.f('ix_user_balances_id'), table_name='user_balances')
    op.drop_table('user_balances')
    op.drop_index(op.f('ix_transactions_id'), table_name='transactions')
    op.drop_table('transactions')
    # ### end Alembic commands ###
