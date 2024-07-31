# backend/Dockerfile
FROM python:3.11

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY new/ . 

# Exposer le port sur lequel Django sera servi
EXPOSE 8000

# Commande par défaut pour démarrer l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "new.wsgi:application"]
