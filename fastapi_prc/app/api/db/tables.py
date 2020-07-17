import sqlalchemy
from .init_db import metadata


Users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, index=True),
    sqlalchemy.Column("email", sqlalchemy.String(128)),
    sqlalchemy.Column("password_hash", sqlalchemy.String(128)),
    sqlalchemy.Column("birth", sqlalchemy.Date),
)


