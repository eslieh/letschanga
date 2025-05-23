"""upgrade db with notifications and user_info models

Revision ID: e88bb35b29a5
Revises: 4a25d62b75fb
Create Date: 2025-05-04 00:25:20.277748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e88bb35b29a5'
down_revision = '4a25d62b75fb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('push_notification_subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('subscription_id', sa.String(length=255), nullable=False),
    sa.Column('device_type', sa.String(length=50), nullable=False),
    sa.Column('endpoint', sa.String(length=255), nullable=True),
    sa.Column('auth_token', sa.String(length=255), nullable=True),
    sa.Column('p256dh', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_push_notification_subscriptions'))
    )
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=True),
    sa.Column('source', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_notifications_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_notifications'))
    )
    op.create_table('user_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('tagline', sa.String(length=255), nullable=True, comment="User's short description"),
    sa.Column('bio', sa.Text(), nullable=True, comment="User's biography"),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_info_user_id_users'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_info'))
    )
    with op.batch_alter_table('user_info', schema=None) as batch_op:
        batch_op.create_index('idx_user_info_user', ['user_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_info_user_id'), ['user_id'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_info', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_info_user_id'))
        batch_op.drop_index('idx_user_info_user')

    op.drop_table('user_info')
    op.drop_table('notifications')
    op.drop_table('push_notification_subscriptions')
    # ### end Alembic commands ###
