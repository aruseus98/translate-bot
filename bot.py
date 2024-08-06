import discord
from googletrans import Translator
from dotenv import load_dotenv
import os
import logging
import re

# Configurer la journalisation
logging.basicConfig(level=logging.INFO, filename='/app/logs/bot.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Obtenir les configurations depuis les variables d'environnement
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID'))
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))

# Initialisation du client Discord et du traducteur
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
client = discord.Client(intents=intents)
translator = Translator()

# Définir l'événement pour quand le bot est prêt
@client.event
async def on_ready():
    logger.info(f'Logged in as {client.user}')
    logger.info(f'Source Channel ID: {SOURCE_CHANNEL_ID}')
    logger.info(f'Target Channel ID: {TARGET_CHANNEL_ID}')

# Fonction pour préserver et restaurer les URLs
def preserve_urls(text):
    url_pattern = re.compile(r'(https?://\S+|http?://\S+)')
    urls = url_pattern.findall(text)
    placeholders = [f'URL_PLACEHOLDER_{i}' for i in range(len(urls))]
    for placeholder, url in zip(placeholders, urls):
        text = text.replace(url, placeholder)
    return text, urls, placeholders

# Fonction pour réinsérer les URLs dans le texte traduit
def restore_urls(translated_text, urls, placeholders):
    for placeholder, url in zip(placeholders, urls):
        translated_text = translated_text.replace(placeholder, url)
    return translated_text

# Fonction pour préserver et restaurer les hashtags
def preserve_and_restore_hashtags(text, translated_text):
    hashtag_pattern = re.compile(r'(\#[^\s]+)')
    hashtags = hashtag_pattern.findall(text)
    placeholders = [f'HASHTAG_PLACEHOLDER_{i}' for i in range(len(hashtags))]
    for placeholder, hashtag in zip(placeholders, hashtags):
        text = text.replace(hashtag, placeholder)
    for placeholder, hashtag in zip(placeholders, hashtags):
        translated_text = translated_text.replace(placeholder, hashtag)
    return translated_text

# Fonction pour préserver et restaurer les liens spéciaux
def preserve_special_links(text):
    special_link_pattern = re.compile(r'\[↧\]\((https?://\S+|http?://\S+)\)|\[▻\]\((https?://\S+|http?://\S+)\)')
    special_links = special_link_pattern.findall(text)
    placeholders = [f'SPECIAL_LINK_PLACEHOLDER_{i}' for i in range(len(special_links))]
    for placeholder, link in zip(placeholders, special_links):
        text = text.replace(f'[↧]({link})', placeholder) if f'[↧]({link})' in text else text.replace(f'[▻]({link})', placeholder)
    return text, special_links, placeholders

def restore_special_links(translated_text, special_links, placeholders):
    for placeholder, link in zip(placeholders, special_links):
        translated_text = translated_text.replace(placeholder, f'[↧]({link})') if '↧' in placeholder else translated_text.replace(placeholder, f'[▻]({link})')
    return translated_text

# Fonction pour détecter la langue du texte
def detect_language(text):
    return translator.detect(text).lang

# Définir l'événement pour quand un nouveau message est envoyé
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

                        # Envoyer le nouvel embed avec la traduction dans le canal cible
                        if target_channel:
                            logger.info(f"Sending embed to target channel: {TARGET_CHANNEL_ID}")
                            await target_channel.send(f'Translation (accurate at 90%):\n{translation}')
                        else:
                            logger.error(f"Target channel with ID {TARGET_CHANNEL_ID} not found")
                    except Exception as e:
                        logger.error(f"Error translating embed: {e}")
                else:
                    logger.info("No description in embed")
        else:
            logger.info("No embed in message")

# Démarrer le bot avec le token
client.run(DISCORD_TOKEN)
