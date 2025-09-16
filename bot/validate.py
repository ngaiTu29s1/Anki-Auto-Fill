# validate.py: Xử lý tách và validate từ
import re

def split_words(text):
	"""
	Tách các từ từ chuỗi, loại bỏ khoảng trắng, ký tự thừa.
	Ví dụ: 'banana, apple, fish' -> ['banana', 'apple', 'fish']
	"""
	# Loại bỏ command nếu có
	if text.startswith('!nw'):
		text = text[3:]
	# Tách theo dấu phẩy, loại bỏ khoảng trắng thừa
	words = [w.strip() for w in text.split(',') if w.strip()]
	# Lọc các từ chỉ chứa ký tự chữ cái (có thể mở rộng)
	words = [w for w in words if re.match(r'^[a-zA-Z\- ]+$', w)]
	return words

def validate_word(word):
	"""
	Validate cơ bản: chỉ nhận từ có ký tự chữ cái, không rỗng.
	Có thể mở rộng thêm logic nâng cao hoặc gọi AI.
	"""
	return bool(re.match(r'^[a-zA-Z\- ]+$', word))
