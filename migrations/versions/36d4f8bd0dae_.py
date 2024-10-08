"""empty message

Revision ID: 36d4f8bd0dae
Revises: 
Create Date: 2024-09-28 21:06:32.344711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36d4f8bd0dae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('questions')
    op.drop_table('semesters')
    op.drop_table('papers')
    op.drop_table('years')
    op.drop_table('units')
    op.drop_table('answers')
    op.drop_table('users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), nullable=False),
    sa.Column('password', sa.VARCHAR(length=255), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('answers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('content', sa.VARCHAR(), nullable=False),
    sa.Column('upvotes', sa.INTEGER(), nullable=True),
    sa.Column('downvotes', sa.INTEGER(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('question_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('units',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('unit_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('year_id', sa.INTEGER(), nullable=False),
    sa.Column('semester_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['semester_id'], ['semesters.id'], ),
    sa.ForeignKeyConstraint(['year_id'], ['years.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('years',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=50), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('papers',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('paper_name', sa.VARCHAR(length=1000), nullable=False),
    sa.Column('year_id', sa.INTEGER(), nullable=False),
    sa.Column('semester_id', sa.INTEGER(), nullable=False),
    sa.Column('unit_id', sa.INTEGER(), nullable=False),
    sa.Column('latex_content', sa.VARCHAR(), nullable=True),
    sa.Column('pdf_path', sa.VARCHAR(), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['semester_id'], ['semesters.id'], ),
    sa.ForeignKeyConstraint(['unit_id'], ['units.id'], ),
    sa.ForeignKeyConstraint(['year_id'], ['years.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('semesters',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('sem_number', sa.INTEGER(), nullable=False),
    sa.Column('year_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['year_id'], ['years.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questions',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('content', sa.VARCHAR(), nullable=False),
    sa.Column('paper_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['paper_id'], ['papers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
