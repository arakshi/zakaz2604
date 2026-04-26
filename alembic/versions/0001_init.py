"""init

Revision ID: 0001_init
Revises: 
Create Date: 2026-04-26
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("roles", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(50), unique=True))
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("full_name", sa.String(120)), sa.Column("email", sa.String(120), unique=True), sa.Column("password_hash", sa.String(255)), sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id")), sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")), sa.Column("created_at", sa.DateTime()))
    op.create_table("clients", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("company_name", sa.String(150)), sa.Column("contact_person", sa.String(120)), sa.Column("phone", sa.String(30)), sa.Column("email", sa.String(120)), sa.Column("segment", sa.String(80)), sa.Column("source", sa.String(80)), sa.Column("created_at", sa.DateTime()))
    op.create_table("deal_stages", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(80), unique=True), sa.Column("sort_order", sa.Integer()))
    op.create_table("deals", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(150)), sa.Column("client_id", sa.Integer(), sa.ForeignKey("clients.id")), sa.Column("manager_id", sa.Integer(), sa.ForeignKey("users.id")), sa.Column("stage_id", sa.Integer(), sa.ForeignKey("deal_stages.id")), sa.Column("amount", sa.Numeric(14,2)), sa.Column("probability", sa.Float()), sa.Column("planned_close_date", sa.Date()), sa.Column("status", sa.String(30)), sa.Column("created_at", sa.DateTime()), sa.Column("updated_at", sa.DateTime()))
    op.create_table("tasks", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(150)), sa.Column("description", sa.Text()), sa.Column("assigned_to", sa.Integer(), sa.ForeignKey("users.id")), sa.Column("related_deal_id", sa.Integer(), sa.ForeignKey("deals.id"), nullable=True), sa.Column("due_date", sa.Date()), sa.Column("status", sa.String(30)), sa.Column("priority", sa.String(20)), sa.Column("created_at", sa.DateTime()))
    op.create_table("notifications", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")), sa.Column("text", sa.String(255)), sa.Column("type", sa.String(40)), sa.Column("is_read", sa.Boolean(), server_default=sa.text("false")), sa.Column("created_at", sa.DateTime()))
    op.create_table("kpi_records", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")), sa.Column("period_start", sa.Date()), sa.Column("period_end", sa.Date()), sa.Column("deals_count", sa.Integer()), sa.Column("closed_amount", sa.Numeric(14,2)), sa.Column("conversion_rate", sa.Float()), sa.Column("avg_cycle_days", sa.Float()))
    op.create_table("import_logs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("file_name", sa.String(255)), sa.Column("imported_rows", sa.Integer()), sa.Column("status", sa.String(20)), sa.Column("created_at", sa.DateTime()))


def downgrade() -> None:
    for table in ["import_logs", "kpi_records", "notifications", "tasks", "deals", "deal_stages", "clients", "users", "roles"]:
        op.drop_table(table)
