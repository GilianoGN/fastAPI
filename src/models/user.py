import sqlalchemy as sa
from src.database import metadata


users = sa.Table(
    "users", metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(150), nullable=False, unique=True),
    sa.Column("password", sa.String, nullable=False),
    )
