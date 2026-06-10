# ADR-003 - Base de données SQLite isolée par service

| Champ       | Valeur                        |
|-------------|-------------------------------|
| **Date**    | 2025-05-01                    |
| **Statut**  | Accepté                       |
| **Auteurs** | Équipe devarch                |

---

## Contexte

Dans une architecture microservices, la gestion des données est un choix architectural fondamental. Trois patterns principaux existent :

- **Shared Database** : tous les services partagent une seule instance de base de données
- **Database per Service** : chaque service possède sa propre base, potentiellement de type différent
- **Event Sourcing** : l'état est reconstitué depuis un journal d'événements

Pour devarch, le contexte est un environnement de développement local avec Docker Compose, sans exigences de haute disponibilité ni de volumes de données importants. La priorité est la **simplicité opérationnelle** et l'**isolation des domaines**.

---

## Décision

**Utiliser SQLite comme base de données, avec une instance isolée par service.**

Chaque service qui nécessite de la persistance embarque son propre fichier `.db` dans son répertoire `db/` :

- `auth-service/db/auth.db` → données utilisateurs, credentials
- `content-service/db/articles.db` → articles, catégories, commentaires
- `media-service/db/` → métadonnées des fichiers media

Chaque service est responsable de son propre schéma (`db/schema.sql`), de son initialisation (`db/init_db.py`) et de ses données de test (`db/seed.sql`).

---

## Conséquences

### Avantages

- **Isolation totale des domaines** : un service ne peut pas lire directement la base d'un autre — la communication passe obligatoirement par les APIs.
- **Zéro infrastructure externe** : pas de serveur PostgreSQL/MySQL à démarrer, SQLite est embarqué dans le processus Python.
- **Simplicité de développement** : `connection.py` dans chaque service suffit, pas de gestion de pool de connexions complexe.
- **Cohérence avec les principes microservices** : chaque service est autonome et déployable indépendamment.
- **Fichiers versionnables** : `schema.sql` et `seed.sql` sont dans le repo, ce qui facilite la revue de code.

### Inconvénients

- **Non adapté à la production** : SQLite ne supporte pas les écritures concurrentes à haute fréquence, ni la réplication, ni les connexions réseau.
- **Pas de transactions inter-services** : une opération métier qui touche plusieurs services (ex. : créer un article + notifier l'auteur) ne peut pas être atomique sans saga pattern.
- **Requêtes cross-service impossibles** : pour des agrégations qui nécessitent des données de plusieurs services, il faut passer par les APIs (N+1 potentiel).
- **Migration de schéma manuelle** : sans Alembic ou outil équivalent, les migrations doivent être gérées à la main via `init_db.py`.

### Neutrales

- En cas d'évolution vers un environnement de production, la migration vers PostgreSQL par service serait la voie naturelle, sans changer l'architecture globale (Database per Service reste valide).
- Le `consumer-service` n'a pas de base de données propre : il consomme des événements RabbitMQ et délègue la persistance aux autres services — ce qui est un choix cohérent pour un service purement événementiel.

---

## Alternatives considérées

| Option | Raison du rejet |
|--------|-----------------|
| PostgreSQL partagé (Shared DB) | Couplage fort entre services, anti-pattern microservices |
| PostgreSQL par service | Surcoût opérationnel non justifié en dev local |
| MongoDB | Complexité supplémentaire sans bénéfice pour des données relationnelles |

---

## Références

- Schémas de données : `auth-service/db/schema.sql`, `content-service/db/schema.sql`, `media-service/db/schema.sql`
- Diagramme ERD global : `devarch-erd.mmd` (à la racine du projet)
- Pattern Database per Service : https://microservices.io/patterns/data/database-per-service.html