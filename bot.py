import discord
from googletrans import Translator
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Obtenir les configurations depuis les variables d'environnement
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
SOURCE_CHANNEL_ID = int(os.getenv('SOURCE_CHANNEL_ID'))
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))

# Initialisation du client Discord et du traducteur
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
translator = Translator()

# Définir l'événement pour quand le bot est prêt
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Définir l'événement pour quand un nouveau message est envoyé
@client.event
async def on_message(message):
    # Ne pas répondre à ses propres messages
    if message.author == client.user:
        return
    
    # Vérifier si le message provient du canal spécifié
    if message.channel.id == SOURCE_CHANNEL_ID:
        # Vérifier s'il y a un embed dans le message
        if message.embeds:
            for embed in message.embeds:
                # Extraire la description du embed
                if embed.description:
                    description = embed.description
                    # Traduire le texte en anglais
                    translation = translator.translate(description, src='ja', dest='en').text
                    # Copier l'embed et ajouter la traduction
                    embed_copy = discord.Embed.from_dict(embed.to_dict())
                    # Envoyer le nouvel embed avec la traduction dans le canal cible
                    target_channel = client.get_channel(TARGET_CHANNEL_ID)
                    await target_channel.send(f'Translation:\n{translation}', embed=embed_copy)

# Démarrer le bot avec le token
client.run(DISCORD_TOKEN)
