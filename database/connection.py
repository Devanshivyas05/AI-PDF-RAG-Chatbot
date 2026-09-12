import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# Load .env from project root
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

load_dotenv(
    os.path.join(PROJECT_ROOT, ".env")
)


MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1").strip()
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306").strip()
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "ragflow_db").strip()
MYSQL_USER = os.getenv("MYSQL_USER", "root").strip()
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "").strip()


# Safely encode username/password
encoded_user = quote_plus(MYSQL_USER)
encoded_password = quote_plus(MYSQL_PASSWORD)


DATABASE_URL = (
    f"mysql+pymysql://"
    f"{encoded_user}:{encoded_password}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
)


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def test_connection():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT DATABASE()")
        )

        database_name = result.scalar()

        print(
            f"MySQL connection successful. "
            f"Database: {database_name}",
            flush=True,
        )

        return database_name