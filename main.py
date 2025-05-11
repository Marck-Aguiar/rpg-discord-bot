from bot import bot
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token is None:
        raise ValueError("Token não encontrado! Verifique se o arquivo .env existe e contém DISCORD_TOKEN")
    bot.run(token)