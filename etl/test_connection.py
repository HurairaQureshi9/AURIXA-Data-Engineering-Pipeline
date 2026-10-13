
from sqlalchemy import URL, create_engine, text
import os


def test_connection():
    password = os.getenv("AURIXA_DB_PASSWORD")

    if not password:
        print("FAIL: MySQL password environment variable is missing.")
        return

    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("AURIXA_DB_USER", "root"),
        password=password,
        host="localhost",
        port=3306,
        database="aurixa_db",
    )

    engine = create_engine(connection_url, pool_pre_ping=True)

    try:
        with engine.connect() as connection:
            database = connection.execute(
                text("SELECT DATABASE()")
            ).scalar_one()

            print(f"SUCCESS: Connected to database '{database}'.")

    except Exception as error:
        print(f"FAIL: Database connection could not be established.")
        print(f"Reason: {error}")

    finally:
        engine.dispose()


if __name__ == "__main__":
    test_connection()
