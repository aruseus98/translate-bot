# translate-bot

This bot is designed to monitor a specified source channel for new messages, translate the content of embedded descriptions, and send both the original and translated content to a target channel. The bot preserves and restores URLs, hashtags, and special links while ignoring specific lines containing "Tweeted" or "Retweeted".  

## Features  

* Monitors a source channel for new messages.  
* Copies the original message content without translation to the target channel.  
* Detects and translates descriptions in message embeds from Japanese to English.  
* Preserves and restores URLs, hashtags, and special links during translation.  
* Skips lines containing "Tweeted" or "Retweeted" in the translation process.  

## Prerequisites

* Python 3.6 or higher  
* Discord.py library  
* googletrans library  
* python-dotenv library  

## Local Setup

1. Clone the repository or download the bot script.  
2. Install the required Python libraries:  

```
pip install discord.py googletrans==4.0.0-rc1 python-dotenv
```

3. Create a .env file in the same directory as the script and add your Discord bot token, source channel ID, and target channel ID:  

```
DISCORD_TOKEN=your_discord_bot_token
SOURCE_CHANNEL_ID=your_source_channel_id
TARGET_CHANNEL_ID=your_target_channel_id
```

4. Run the bot script:  

```
python bot.py
```

## Docker Setup

1. Clone the repository or download the bot script.  
2. Create a .env file in the same directory as the script and add your Discord bot token, source channel ID, and target channel ID:  

```
DISCORD_TOKEN=your_discord_bot_token
SOURCE_CHANNEL_ID=your_source_channel_id
TARGET_CHANNEL_ID=your_target_channel_id
```

3. Build the Docker image:   

```
docker build -t discord-translation-bot .
```

4. Run the Docker container:  

```
docker run -d --name discord-translation-bot discord-translation-bot
```

## Configuration

* DISCORD_TOKEN: Your Discord bot token.  
* SOURCE_CHANNEL_ID: The ID of the channel the bot will monitor for new messages.  
* TARGET_CHANNEL_ID: The ID of the channel where the bot will send the original and translated messages.  

## How It Works

* On Bot Ready: Logs the bot's name and the IDs of the source and target channels.  
* On Message: Listens for new messages in the source channel.  
- Sends the original message content to the target channel without translation.  
- Detects embeds in the message and translates the description from Japanese to English.  
- Sends the translated embed description to the target channel.  

## Logging

* Logs various actions and events, including message reception, content processing, and any errors encountered.  

## Notes

* Ensure the bot has the necessary permissions to read messages in the source channel and send messages in the target channel.  
* The bot only translates embedded descriptions and ignores translating the main content of the message.  
