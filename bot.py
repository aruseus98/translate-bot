import logging
from config.config import DISCORD_TOKEN
from events.events import run_bot

# Configurer la journalisation
logging.basicConfig(level=logging.INFO, filename='/app/logs/bot.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    run_bot(DISCORD_TOKEN)
