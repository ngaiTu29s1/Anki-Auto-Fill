import re
from ai import  ai_validate_word

def split_words(text):
	# ignore command
	if text.startswith('!nw'):
		text = text[3:]
	# comma separated
	words = [w.strip() for w in text.split(',') if w.strip()]
	# Lọc các từ chỉ chứa ký tự chữ cái (có thể mở rộng)
	# words = [w for w in words if re.match(r'^[a-zA-Z\- ]+$', w)]
	return words

def validate_word(word):
	res = ai_validate_word(word)
	print(f"Validation result for '{word}': {res}")
	return res
