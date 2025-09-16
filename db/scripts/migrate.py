
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from db.models.raw_word import Base
from dotenv import load_dotenv
print('sys.path:', sys.path)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env.db'))
DATABASE_URL = os.getenv("DATABASE_URL")


def migrate():
    max_retries = 10
    for i in range(max_retries):
        try:
            engine = create_engine(DATABASE_URL)
            Base.metadata.create_all(engine)
            print("Migration done!")
            return
        except OperationalError as e:
            print(f"DB connection failed (attempt {i+1}/{max_retries}): {e}")
            time.sleep(3)
    print("Migration failed after retries!")
    raise Exception("Could not connect to DB after retries")

if __name__ == "__main__":
    migrate()