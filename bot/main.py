import os
import discord
from dotenv import load_dotenv
from validate import split_words, validate_word
from ai import get_definitions, format_results
from db_utils import insert_raw_word, get_raw_words
from db.models.raw_word import WordStatus, RawWord


# environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), './.env.bot.dev'))
TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))

# init bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # Ready event
    print(f'{client.user} has connected to Discord!')
    print('-----------------------------------------')

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id != TARGET_CHANNEL_ID:
        return

    content = message.content.strip()
    print("Received message:", content)
    if content.startswith('!help'):
        await message.channel.send("Instructions is coming soon...")

    elif content.startswith('!nw'):
        words = split_words(content)
        if not words:
            await message.channel.send("Cannot find any words to define.")
            return
        valid_words = []
        invalid_words = []
        for w in words:
            if validate_word(w):
                valid_words.append(w)
                insert_raw_word(
                    RawWord,
                    word=w,
                    normalized_word=w.lower().strip(),
                    status=WordStatus.QUEUED,
                    lang='en'
                )
            else:
                invalid_words.append(w)
        if valid_words:
            try:
                results = await get_definitions(valid_words)
                print(results)
                output = format_results(valid_words, results)
            except Exception as e:
                output = f"Error: {e}"
            await message.channel.send(output)
        if invalid_words:
            await message.channel.send(f"Các từ sau không hợp lệ: {', '.join(f'`{w}`' for w in invalid_words)}")

    elif content.startswith('!get'):
        words = get_raw_words()
        await message.channel.send("Fetched words:\n" + "\n".join(f"{i+1}. {w}" for i, w in enumerate(words)))
    else:
        await message.channel.send("Invalid command. Type !help for usage.")

# Chạy bot
client.run(TOKEN)