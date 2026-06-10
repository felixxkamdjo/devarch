#!/bin/sh
# auth-service/entrypoint.sh
set -e

echo "--- Auth service starting ---"

# Appliquer le schema
COUNT=$(python db/init_db.py | tail -1)

#  Seed uniquement si la table est vide
if [ "$COUNT" = "0" ]; then
    echo "- Database empty — running seed..."
    python db/seed.py
else
    echo "- Database has $COUNT user(s) — skipping seed"
fi

# Démarrer le serveur
echo "- Starting server..."
exec python server.py