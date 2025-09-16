import google.generativeai as genai
import os
from dotenv import load_dotenv


# config
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env.bot'))
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