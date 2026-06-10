#!/bin/sh
# content-service/entrypoint.sh
set -e

echo "--- Content service starting ---"

# Appliquer le schema
echo "- Applying schema..."
COUNT=$(python db/init_db.py | tail -1)

# Seed uniquement si la table est vide
if [ "$COUNT" = "0" ]; then
    echo "- Database empty — running seed..."
    python db/seed.py
else
    echo "- Database has $COUNT article(s) — skipping seed"
fi

#  Démarrer le serveur
echo "- Starting server..."
exec python server.py