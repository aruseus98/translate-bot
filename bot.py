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

# Fonction pour détecter et exclure les URLs
def preserve_urls(text):
    url_pattern = re.compile(r'(https?://\S+)')
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

# Fonction pour préserver et restaurer les hashtags s'ils ne sont pas des liens
def preserve_and_restore_hashtags(text, translated_text):
    hashtag_pattern = re.compile(r'(\s#[^\s]+)')
    hashtags = hashtag_pattern.findall(text)
    for hashtag in hashtags:
        if hashtag not in text:
            continue
        translated_text = translated_text.replace(f'HASHTAG_PLACEHOLDER_{hashtags.index(hashtag)}', hashtag)
    return translated_text

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

        # Traiter les messages normaux
        if message.content:
            try:
                logger.info("Processing normal message")
                text, urls, url_placeholders = preserve_urls(message.content)
                translation = translator.translate(text, src='ja', dest='en').text
                translation = restore_urls(translation, urls, url_placeholders)
                translation = preserve_and_restore_hashtags(message.content, translation)
                logger.info(f"Translation: {translation}")
                target_channel = client.get_channel(TARGET_CHANNEL_ID)
                if target_channel:
                    logger.info(f"Sending message to target channel: {TARGET_CHANNEL_ID}")
                    # Envoyer le message original d'abord
                    await target_channel.send(message.content)
                    # Ensuite, envoyer la traduction
                    await target_channel.send(f'Translation:\n{translation}')
                else:
                    logger.error(f"Target channel with ID {TARGET_CHANNEL_ID} not found")
            except Exception as e:
                logger.error(f"Error translating message: {e}")

        # Vérifier s'il y a un embed dans le message
        if message.embeds:
            logger.info("Embed detected")
            for embed in message.embeds:
                # Extraire la description du embed
                if embed.description:
                    try:
                        description = embed.description
                        logger.info(f"Embed description: {description}")
                        
                        # Préserver les URLs dans la description de l'embed
                        text, urls, url_placeholders = preserve_urls(description)
                        
                        # Traduire le texte en anglais
                        translation = translator.translate(text, src='ja', dest='en').text
                        translation = restore_urls(translation, urls, url_placeholders)
                        translation = preserve_and_restore_hashtags(description, translation)
                        logger.info(f"Translation: {translation}")
                        
                        # Copier l'embed et ajouter la traduction
                        embed_copy = discord.Embed.from_dict(embed.to_dict())
                        
                        # Envoyer le nouvel embed avec la traduction dans le canal cible
                        target_channel = client.get_channel(TARGET_CHANNEL_ID)
                        if target_channel:
                            logger.info(f"Sending embed to target channel: {TARGET_CHANNEL_ID}")
                            await target_channel.send(embed=embed_copy)
                            await target_channel.send(f'Translation:\n{translation}')
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
