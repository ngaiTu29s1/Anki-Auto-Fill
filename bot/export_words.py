import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from db.models.raw_word import RawWord
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), './.env.bot.dev'))
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def get_all_normalized_words():
    session = Session()
    try:
        # Lấy tất cả normalized_word, loại trùng lặp
        words = session.query(RawWord.normalized_word).distinct().all()
        return [w[0] for w in words]
    finally:
        session.close()

if __name__ == "__main__":
    words = get_all_normalized_words()
    print("Normalized words:")
    for w in words:
        print(w)
