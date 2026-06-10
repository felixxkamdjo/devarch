# devarch

Plateforme de blog headless construite en architecture microservices.  
Backend Python 3.12 stdlib-only · Frontend HTML/CSS/JS vanilla · Docker Compose · RabbitMQ

---

## Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Architecture](#architecture)
- [Prérequis](#prérequis)
- [Démarrage rapide](#démarrage-rapide)
- [Services](#services)
- [API](#api)
- [Tests](#tests)
- [Structure du projet](#structure-du-projet)
- [Documentation](#documentation)

---

## Vue d'ensemble

devarch est une plateforme de blog headless où le frontend et le backend sont totalement découplés. Le backend expose une API REST via un API Gateway centralisé, et les services communiquent entre eux soit en HTTP interne, soit de manière asynchrone via RabbitMQ.

**Stack technique :**

| Couche | Technologie |
|--------|-------------|
| Backend services | Python 3.13 (stdlib uniquement) |
| Frontend | HTML + CSS + JavaScript ES6+ |
| Reverse proxy / Gateway | nginx |
| Base de données | SQLite (isolée par service) |
| Message broker | RabbitMQ |
| Orchestration | Docker Compose |

---

## Architecture

```
Client (navigateur)
        │
        ▼
  ┌─────────────┐        ┌─────────────┐
  │  front-end  │        │ api-gateway │  ← point d'entrée unique de l'API
  │  nginx:8080 │───────▶│  nginx+py   │
  └─────────────┘        │    :8000    │
                         └──────┬──────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
      ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
      │ auth-service  │ │content-service│ │ media-service │
      │   auth.db     │ │  articles.db  │ │   media.db    │
      └───────────────┘ └───────┬───────┘ └───────────────┘
                                │ publie événements
                                ▼
                         ┌─────────────┐
                         │  RabbitMQ   │
                         └──────┬──────┘
                                │ consomme
                                ▼
                       ┌─────────────────┐
                       │consumer-service │
                       └─────────────────┘
```

**Flux d'une requête authentifiée :**

1. Le frontend envoie une requête HTTP vers `api-gateway` (port 8000)
2. `api-gateway` route vers le service cible selon le préfixe de l'URL
3. Le service cible appelle `auth-service` en HTTP interne pour valider le JWT
4. Le service traite la requête et retourne la réponse

Les diagrammes C4 (Context, Container, Component) sont disponibles dans [`docs/architecture/`](./docs/architecture/).

---

## Prérequis

- [Docker](https://docs.docker.com/get-docker/) ≥ 24
- [Docker Compose](https://docs.docker.com/compose/) ≥ 2.20
- [Make](https://www.gnu.org/software/make/) (optionnel, pour les raccourcis)
- [Python 3.13](https://www.python.org/) + [pytest](https://pytest.org/) (pour les tests en local)

---

## Démarrage rapide

```bash
# Cloner le dépôt
git clone https://formuloo.com/devarch.git
cd devarch

# Démarrer toute la stack
make up
# ou
docker compose up --build

# Arrêter la stack
make down
# ou
docker compose down
```

Une fois démarrée :

| Interface | URL |
|-----------|-----|
| Frontend (blog) | http://localhost:8080 |
| API Gateway | http://localhost:8000 |
| RabbitMQ Dashboard | http://localhost:15672 |

Identifiants RabbitMQ par défaut : `guest` / `guest`

---

## Services

### `api-gateway` - Port 8000

Point d'entrée unique de l'API. Route les requêtes selon le préfixe :

| Préfixe URL | Service cible |
|-------------|---------------|
| `/auth/*` | `auth-service` |
| `/articles/*`, `/categories/*`, `/comments/*` | `content-service` |
| `/media/*`, `/upload/*` | `media-service` |

### `auth-service`

Gestion des utilisateurs et authentification JWT.  
Endpoints : `POST /auth/register` · `POST /auth/login` · `GET /auth/me`  
Base de données : `auth-service/db/auth.db`

### `content-service`

Gestion des articles, catégories et commentaires.  
Publie des événements sur RabbitMQ après chaque opération sur les articles.  
Base de données : `content-service/db/articles.db`

### `media-service`

Upload et stockage des fichiers (images, vidéos, binaires).  
Les fichiers sont stockés dans `media-service/storage/`.  
Base de données : `media-service/db/media.db`

### `consumer-service`

Consommateur RabbitMQ pur — pas de base de données ni d'endpoints HTTP.  
Traite les événements publiés par `content-service`.

### `front-end` — Port 8080

Interface utilisateur servie par nginx.  
Pages : `home`, `article`, `editor`, `login`, `signup`

---

## API

La documentation complète de l'API est disponible dans [`docs/api/`](./docs/api/) :

- **Swagger/OpenAPI** : [`docs/api/openapi.yaml`](./docs/api/openapi.yaml)  
  → Visualiser sur [editor.swagger.io](https://editor.swagger.io) (File → Import File)

- **Collection Postman** : [`docs/api/devarch.postman_collection.json`](./docs/api/devarch.postman_collection.json)  
  → Importer dans Postman (Import → Upload Files)

### Authentification

Les endpoints protégés nécessitent un header `Authorization` :

```
Authorization: Bearer <token>
```

Le token est retourné par `/auth/login` et `/auth/register`.  
Dans la collection Postman, il est sauvegardé automatiquement dans la variable `{{token}}` après chaque login ou inscription.

### Exemple rapide

```bash
# Inscription
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"user_firstname":"Félix","user_lastname":"Kamdjo","email":"felix@devarch.io","password":"s3cr3tP@ss"}'

# Lister les articles
curl http://localhost:8000/articles?page=1&limit=9

# Créer un article (token requis)
curl -X POST http://localhost:8000/articles \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title":"Mon article","content":"Contenu...","category_id":1}'
```

---

## Tests

Le projet contient trois niveaux de tests :

```bash
# Lancer tous les tests
pytest

# Tests unitaires uniquement
pytest tests/unit/

# Tests d'intégration
pytest tests/integration/

# Tests de contrat (Pact)
pytest tests/contract/
```

**Structure des tests :**

| Dossier | Type | Ce qui est testé |
|---------|------|------------------|
| `tests/unit/` | Unitaire | Services, JWT, sécurité |
| `tests/integration/` | Intégration | Auth, content, media end-to-end |
| `tests/contract/` | Contrat (Pact) | Interface content ↔ auth |

Dépendances de test : `tests/requirements-test.txt`

```bash
pip install -r tests/requirements-test.txt
```

---

## Structure du projet

```
devarch/
├── api-gateway/          # Point d'entrée HTTP + nginx
├── auth-service/         # Authentification JWT
├── content-service/      # Articles, catégories, commentaires
├── media-service/        # Upload et stockage de fichiers
├── consumer-service/     # Consommateur RabbitMQ
├── front-end/            # Interface utilisateur (nginx + static)
├── tests/
│   ├── unit/             # Tests unitaires
│   ├── integration/      # Tests d'intégration
│   └── contract/         # Tests de contrat Pact
├── docs/
│   ├── adr/              # Architecture Decision Records
│   ├── architecture/     # Diagrammes C4 (PlantUML)
│   └── api/              # OpenAPI + Collection Postman
├── devarch-erd.mmd       # Diagramme ERD (Mermaid)
├── docker-compose.yml
└── Makefile
```

Chaque service suit la même structure interne :

```
{service}/
├── db/                   # Schéma SQL, init, seeds
├── handlers/             # Couche HTTP (parsing requête, réponse)
├── services/             # Logique métier
├── repositories/         # Accès aux données (SQL)
├── utils/                # Helpers HTTP, JWT, sécurité
├── server.py             # Point d'entrée du service
├── router.py             # Routage des requêtes
├── Dockerfile
└── requirements.txt
```

---

## Documentation

| Document | Chemin | Description |
|----------|--------|-------------|
| ADR-001 | [`docs/adr/ADR-001-stdlib-only-backend.md`](./docs/adr/ADR-001-stdlib-only-backend.md) | Choix stdlib Python uniquement |
| ADR-002 | [`docs/adr/ADR-002-nginx-api-gateway.md`](./docs/adr/ADR-002-nginx-api-gateway.md) | nginx comme API Gateway |
| ADR-003 | [`docs/adr/ADR-003-sqlite-database-per-service.md`](./docs/adr/ADR-003-sqlite-database-per-service.md) | SQLite isolée par service |
| C4 Niveau 1 | [`docs/architecture/C4-L1-context.puml`](./docs/architecture/C4-L1-context.puml) | Vue contexte système |
| C4 Niveau 2 | [`docs/architecture/C4-L2-container.puml`](./docs/architecture/C4-L2-container.puml) | Vue conteneurs |
| C4 Niveau 3 | [`docs/architecture/C4-L3-component-content-service.puml`](./docs/architecture/C4-L3-component-content-service.puml) | Vue composants (content-service) |
| OpenAPI | [`docs/api/openapi.yaml`](./docs/api/openapi.yaml) | Spécification Swagger complète |
| Postman | [`docs/api/devarch.postman_collection.json`](./docs/api/devarch.postman_collection.json) | Collection Postman prête à l'emploi |