from db_utils import insert_word, get_raw_words
from ai import get_full_word
from db.models.real_word import RealWord

full_words = get_full_word(get_raw_words())
for w in full_words:
    insert_word(
        table=RealWord,
        word=w['word'],
        phonetic=w['phonetic'],
        english_meaning=w['english_meaning'],
        vietnamese_meaning=w['vietnamese_meaning'],
        example_sentence=w['example_sentence'],
        word_audio=w['word_audio'],
        image=w['image'],
        example_audio=w['example_audio'],
        clean_sentence=w['clean_sentence'],
    )