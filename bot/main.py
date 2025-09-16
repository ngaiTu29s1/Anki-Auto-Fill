import os
import discord
from dotenv import load_dotenv

# environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env.bot'))
TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))

# Khởi tạo bot với các quyền cần thiết
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
    """Sự kiện được gọi mỗi khi có một tin nhắn mới."""
    # Bỏ qua tin nhắn từ chính bot
    if message.author == client.user:
        return

    # Chỉ xử lý tin nhắn trong kênh target
    if message.channel.id != TARGET_CHANNEL_ID:
        return

    word_to_learn = message.content.strip()
    print(f"Nhận được từ mới: '{word_to_learn}' từ người dùng {message.author.name}")

    # --- Giai đoạn AI Validate (sẽ thêm sau) ---
    print(f"Bắt đầu validate từ '{word_to_learn}'...")
    # is_valid = await call_ai_to_validate(word_to_learn)
    is_valid = True # Tạm thời luôn cho là hợp lệ

    if is_valid:
        print(f"Từ '{word_to_learn}' hợp lệ.")
        # --- Giai đoạn ghi vào DB (sẽ thêm sau) ---
        print(f"Chuẩn bị ghi '{word_to_learn}' vào cơ sở dữ liệu...")
        # success = await write_to_database(word_to_learn)

        # Phản hồi lại người dùng
        await message.channel.send(f"Đã nhận và ghi nhận từ: `{word_to_learn}`")
    else:
        print(f"Từ '{word_to_learn}' không hợp lệ.")
        await message.channel.send(f"Từ `{word_to_learn}` có vẻ không hợp lệ. Vui lòng kiểm tra lại.")


# Chạy bot
client.run(TOKEN)