import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models.raw_word import RawWord, WordStatus, Base
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), './.env.bot.dev'))

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def insert_word(word, note=None, status=WordStatus.QUEUED, lang="en"):
    session = Session()
    try:
        normalized_word = word.lower().strip()
        raw_word = RawWord(
            word=word,
            normalized_word=normalized_word,
            lang=lang,
            status=status,
            note=note
        )
        session.add(raw_word)
        session.commit()
        print(f"Inserted word: {word}")
    except Exception as e:
        session.rollback()
        print(f"Error inserting word: {e}")
    finally:
        session.close()
