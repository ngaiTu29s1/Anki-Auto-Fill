
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


def insert_word(table, **kwargs):
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

def get_raw_words(status=WordStatus.QUEUED):
    session = Session()
    try:
        words = session.query(RawWord).filter(RawWord.status == status).all()
        return [w.normalized_word for w in words]
    except Exception as e:
        print(f"Error fetching words: {e}")
        return []
    finally:
        session.close()

def update_raw_word_status(normalized_word, success=True):
    session = Session()
    try:
        word = session.query(RawWord).filter(RawWord.normalized_word == normalized_word).first()
        if word:
            word.status = WordStatus.ENRICHED if success else WordStatus.ERROR
            session.commit()
            print(f"Updated status for {normalized_word} to {word.status}")
        else:
            print(f"Word not found: {normalized_word}")
    except Exception as e:
        session.rollback()
        print(f"Error updating status: {e}")
    finally:
        session.close()