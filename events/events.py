import discord
import asyncio
import logging
from googletrans import Translator
from utils.utils import (
    preserve_urls, restore_urls, 
    preserve_and_restore_hashtags, preserve_special_links, 
    restore_special_links, detect_language
)
from config.config import SOURCE_CHANNEL_ID, TARGET_CHANNEL_ID

logger = logging.getLogger(__name__)
translator = Translator()

# Initialisation du client Discord et du traducteur
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user}')
    logger.info(f'Source Channel ID: {SOURCE_CHANNEL_ID}')
    logger.info(f'Target Channel ID: {TARGET_CHANNEL_ID}')

@client.event
async def on_message(message):
    # Ne pas répondre à ses propres messages
    if message.author == client.user:
        return

    logger.info(f"Message received in channel {message.channel.id}")
    logger.info(f"Message content: {message.content}")
    logger.info(f"Message embeds: {message.embeds}")
    logger.info(f"Message type: {message.type}")
    logger.info(f"Message author: {message.author}")
    logger.info(f"Message ID: {message.id}")

    # Vérifier si le message provient du canal spécifié
    if message.channel.id == SOURCE_CHANNEL_ID:
        logger.info(f"Message detected in source channel: {message.content}")

        target_channel = client.get_channel(TARGET_CHANNEL_ID)
        if not target_channel:
            logger.error(f"Target channel with ID {TARGET_CHANNEL_ID} not found")
            return

        # Envoyer le message original sans le traduire
        if message.content:
            await target_channel.send(message.content)
            await asyncio.sleep(1)  # Ajouter un délai après l'envoi du message original

        # Vérifier s'il y a un embed dans le message
        if message.embeds:
            logger.info("Embed detected")
            for embed in message.embeds:
                # Extraire la description du embed
                if embed.description:
                    try:
                        description = embed.description
                        logger.info(f"Embed description: {description}")

                        # Détecter la langue de la description
                        detected_lang = detect_language(description)
                        logger.info(f"Detected language: {detected_lang}")

                        # Si la langue est l'anglais, ne pas traduire
                        if detected_lang == 'en':
                            logger.info("Text is already in English, skipping translation.")
                            continue

                        # Préserver les URLs et les liens spéciaux dans la description de l'embed
                        text, special_links, special_placeholders = preserve_special_links(description)
                        text, urls, url_placeholders = preserve_urls(text)

                        # Traduire le texte en anglais
                        translation = translator.translate(text, src='ja', dest='en').text
                        translation = restore_urls(translation, urls, url_placeholders)
                        translation = restore_special_links(translation, special_links, special_placeholders)
                        translation = preserve_and_restore_hashtags(description, translation)
                        logger.info(f"Translation: {translation}")

                        # Envoyer la traduction
                        if target_channel:
                            logger.info(f"Sending embed translation to target channel: {TARGET_CHANNEL_ID}")
                            await target_channel.send(f'Translation (accurate at 90%):\n{translation}')
                            await asyncio.sleep(1)  # Ajouter un délai après l'envoi de la traduction
                        else:
                            logger.error(f"Target channel with ID {TARGET_CHANNEL_ID} not found")
                    except Exception as e:
                        logger.error(f"Error translating embed: {e}")
                else:
                    logger.info("No description in embed")
        else:
            logger.info("No embed in message")

# Démarrer le bot avec le token
def run_bot(token):
    client.run(token)
