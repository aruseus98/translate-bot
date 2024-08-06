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
