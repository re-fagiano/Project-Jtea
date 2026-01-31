"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2025-01-31 00:00:00
"""
from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "utenti",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("ruolo", sa.Enum("admin", "supervisore", "tecnico", "cliente", name="userrole"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )
    op.create_index(op.f("ix_utenti_email"), "utenti", ["email"], unique=True)

    op.create_table(
        "clienti",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("nome", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "richieste",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("titolo", sa.String(length=255), nullable=False),
        sa.Column("descrizione", sa.Text(), nullable=True),
        sa.Column("stato", sa.String(length=50), nullable=False),
        sa.Column("cliente_id", sa.String(length=36), nullable=False),
        sa.Column("utente_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["cliente_id"], ["clienti.id"]),
        sa.ForeignKeyConstraint(["utente_id"], ["utenti.id"]),
    )


def downgrade() -> None:
    op.drop_table("richieste")
    op.drop_table("clienti")
    op.drop_index(op.f("ix_utenti_email"), table_name="utenti")
    op.drop_table("utenti")
    op.execute("DROP TYPE IF EXISTS userrole")
