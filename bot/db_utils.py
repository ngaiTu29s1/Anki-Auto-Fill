import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models.raw_word import RawWord, WordStatus, Base
from db.models.real_word import RealWord
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(__file__), './.env.bot.dev'))

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def insert_raw_word(table, **kwargs):
    session = Session()
    try:
        row = table(**kwargs)
        session.add(row)
        session.commit()
        print(f"Inserted word: {row.word}") 
    except Exception as e:
        session.rollback()
        print(f"Error inserting word: {e}")
    finally:
        session.close()

def get_raw_words(status=WordStatus.QUEUED, limit=5):
    session = Session()
    try:
        words = session.query(RawWord).filter(RawWord.status == status).limit(limit).all()
        return [w.normalized_word for w in words]
    except Exception as e:
        print(f"Error fetching words: {e}")
        return []
    finally:
        session.close()