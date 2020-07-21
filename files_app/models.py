import sqlalchemy
from sqlalchemy.dialects import sqlite
from sqlalchemy.schema import CreateTable

metadata = sqlalchemy.MetaData()

File = sqlalchemy.Table(
    "files",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=100)),
)


async def init_db(db):
    query = CreateTable(File).compile(dialect=sqlite.dialect()).string
    query = query.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
    await db.execute(query=query)
