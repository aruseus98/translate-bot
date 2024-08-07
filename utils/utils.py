import re
from googletrans import Translator

translator = Translator()

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
