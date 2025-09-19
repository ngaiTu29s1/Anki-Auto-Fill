import re
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# config
load_dotenv(os.path.join(os.path.dirname(__file__), './.env.bot.dev'))
gemini_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-1.5-flash')

async def get_definitions(words):
    """
    Gửi tất cả các từ trong 1 prompt, nhận về định nghĩa từng từ.
    """
    prompt = (
        "For each of the following words, give a simple English definition. "
        "Format the answer as: 1. word: definition, 2. word: definition, ...\n"
        f"Words: {', '.join(words)}"
    )
    response = await model.generate_content_async(prompt)
    text = response.text.strip()
    # Parse response: mỗi dòng 1. word: definition
    results = []
    for i in range(len(words)):
        prefix = f"{i+1}. "
        line = next((l for l in text.splitlines() if l.strip().startswith(prefix)), None)
        if line:
            parts = line.split(':', 1)
            definition = parts[1].strip() if len(parts) > 1 else ''
        else:
            definition = ''
        results.append(definition)
    return results

def format_results(words, results):
    return '\n'.join(f"{i+1}. {w}: {r}" for i, (w, r) in enumerate(zip(words, results)))

def ai_validate_word(word):
    prompt = (
        'You are an English dictionary validator. For the given word, respond with only one word: VALID if it is a real, meaningful English word, or INVALID if it is not. Do not explain or add anything else. Word: "{}"'
    ).format(word)
    response = model.generate_content(prompt)
    result = response.text.strip().upper()
    return result == "VALID"

def get_full_word(words):
    prompt = (
        """For each input word, output ONE JSON object with exactly these fields:
        - word: the input word (string)
        - phonetic: IPA transcription (string, e.g. "/ˈæp.l̩/")
        - english_meaning: ONE short, simple English definition (<=15 words)
        - vietnamese_meaning: ONE concise Vietnamese translation (<=8 words)
        - example_sentence: ONE simple sentence using the word (<=15 words, A1–B1 level)
        - word_audio: always leave empty string ""
        - image: always leave empty string ""
        - example_audio: always leave empty string ""
        - clean_sentence: leave empty string ""

        Rules:
        - Return ONLY valid JSON array.
        - Exactly one object per input word, with fields in snake_case as listed.
        - example_sentence must be natural, useful for learners.
        - If you are unsure about any field, leave it as "".
        Do not include any markdown or code block markers. Output only the JSON array, nothing else.
        """
        f"Input words: {', '.join(words)}"
    )
    response = model.generate_content(prompt)
    text = response.text.strip()
    text_json = json.loads(text)
    print(text_json, type(text_json[0]))
    # Parse response: mỗi dòng 1. word: definition
    results = []
    for i in range(len(words)):
        prefix = f"{i+1}. "
        line = next((l for l in text.splitlines() if l.strip().startswith(prefix)), None)
        if line:
            parts = line.split(':', 1)
            definition = parts[1].strip() if len(parts) > 1 else ''
        else:
            definition = ''
        results.append(definition)
    return results

get_full_word(["example", "test"])