import databases
from sqlalchemy import create_engine, MetaData

SQLALCHEMY_DATABASE_URL = "sqlite:///./ab180.db"#os.getenv("DB_CONN")
database = databases.Database(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata.create_all(engine)

