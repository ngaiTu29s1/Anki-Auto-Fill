import os
import discord
from dotenv import load_dotenv
from validate import split_words, validate_word

# environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env.bot'))
TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# init bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Sự kiện được gọi khi bot đã kết nối thành công với Discord."""
    print(f'{client.user} đã kết nối với Discord!')
    print('-----------------------------------------')

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id != TARGET_CHANNEL_ID:
        return

    content = message.content.strip()
    if content.startswith('!nw'):
        words = split_words(content)
        if not words:
            await message.channel.send("Không tìm thấy từ hợp lệ nào.")
            return
        valid_words = [w for w in words if validate_word(w)]
        invalid_words = [w for w in words if not validate_word(w)]
        # Ghi nhận các từ hợp lệ (sau này sẽ ghi DB)
        if valid_words:
            await message.channel.send(f"Đã nhận và ghi nhận các từ: {', '.join(f'`{w}`' for w in valid_words)}")
        if invalid_words:
            await message.channel.send(f"Các từ sau không hợp lệ: {', '.join(f'`{w}`' for w in invalid_words)}")
    else:
        # Xử lý như cũ nếu không phải command !nw
        word_to_learn = content
        print(f"Nhận được từ mới: '{word_to_learn}' từ người dùng {message.author.name}")
        if validate_word(word_to_learn):
            print(f"Từ '{word_to_learn}' hợp lệ.")
            await message.channel.send(f"Đã nhận và ghi nhận từ: `{word_to_learn}`")
        else:
            print(f"Từ '{word_to_learn}' không hợp lệ.")
            await message.channel.send(f"Từ `{word_to_learn}` có vẻ không hợp lệ. Vui lòng kiểm tra lại.")

# Chạy bot
client.run(TOKEN)