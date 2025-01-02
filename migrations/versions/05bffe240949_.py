"""empty message

Revision ID: 05bffe240949
Revises: 0ecd67cdc21b
Create Date: 2025-01-02 12:42:27.678534

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05bffe240949'
down_revision = '0ecd67cdc21b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('fav_people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('people_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['people_id'], ['people.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('fav_planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('planet_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['planet_id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.alter_column('height',
               existing_type=sa.NUMERIC(),
               type_=sa.Float(),
               existing_nullable=False)

    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('diameter',
               existing_type=sa.NUMERIC(),
               type_=sa.Float(),
               existing_nullable=False)
        batch_op.alter_column('orbital_period',
               existing_type=sa.NUMERIC(),
               type_=sa.Float(),
               existing_nullable=False)
        batch_op.alter_column('gravity',
               existing_type=sa.NUMERIC(),
               type_=sa.Float(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.alter_column('gravity',
               existing_type=sa.Float(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.alter_column('orbital_period',
               existing_type=sa.Float(),
               type_=sa.NUMERIC(),
               existing_nullable=False)
        batch_op.alter_column('diameter',
               existing_type=sa.Float(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.alter_column('height',
               existing_type=sa.Float(),
               type_=sa.NUMERIC(),
               existing_nullable=False)

    op.drop_table('fav_planets')
    op.drop_table('fav_people')
    # ### end Alembic commands ###
