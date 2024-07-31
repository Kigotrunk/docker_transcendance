# frontend/Dockerfile
FROM node:18

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de package
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code de l'application
COPY . .

# Construire l'application
RUN npm run build

# Exposer le port sur lequel l'application sera servie
EXPOSE 3000

# Commande par défaut pour démarrer l'application
CMD ["npm", "start"]


