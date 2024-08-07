# Utiliser une image Python comme base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers du projet, y compris .env
COPY . .

# Créer le répertoire des logs
RUN mkdir -p /app/logs

# Commande pour démarrer le bot
CMD ["python", "bot.py"]
