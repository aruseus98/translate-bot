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
