"""Running the chatbot locally.

The bot requires of a replicate token. It is recommended to store it at a .env
file as REPLICATE_TOKEN. This is the current approach taken here.

This token can be user-generated here: https://replicate.com/account
"""

import dotenv
from bot import ChatBot

if __name__ == "__main__":
    dotenv.load_dotenv(".env")
    bot = ChatBot()
    bot.run_on_terminal()
