# 

# nginx:alpine sert directement les fichiers.
FROM nginx:alpine

# Supprimer la page nginx par défaut
RUN rm -rf /usr/share/nginx/html/*

# Copier les sources statiques
COPY . /usr/share/nginx/html

# Config nginx 
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -qO- http://localhost/health || exit 1

CMD ["nginx", "-g", "daemon off;"]