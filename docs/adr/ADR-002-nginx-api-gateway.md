# ADR-002 - nginx comme API Gateway et point d'entrée unique

| Champ       | Valeur                        |
|-------------|-------------------------------|
| **Date**    | 2025-05-01                    |
| **Statut**  | Accepté                       |
| **Auteurs** | Équipe devarch                |

---

## Contexte

Dans une architecture microservices, les clients (navigateurs, applications mobiles) ne doivent pas connaître l'adresse interne de chaque service. Il faut un **point d'entrée unique** qui :

1. Route les requêtes vers le bon service selon le chemin de l'URL
2. Masque la topologie interne du réseau
3. Peut gérer les politiques transversales (CORS, rate limiting, TLS)

Deux approches ont été envisagées :

- **Option A** : Un service gateway applicatif custom en Python (déjà présent dans `api-gateway/` avec `server.py`, `router.py`, `handlers/gateway.py`, `services/proxy.py`)
- **Option B** : nginx en reverse proxy direct, configuré via `nginx.conf`

L'arborescence révèle que **les deux coexistent** : `api-gateway/` contient un serveur Python ET un `nginx.conf`. L'architecture finale a retenu nginx comme couche de routage principale, le code Python assurant la logique de proxy applicative derrière nginx.

---

## Décision

**Utiliser nginx comme API Gateway** pour le routage HTTP entrant, avec le service `api-gateway` Python comme couche applicative intermédiaire gérant la logique de proxy (forwarding, manipulation des headers, gestion des erreurs de routage).

nginx route vers `api-gateway`, qui dispatche ensuite vers les services cibles (`auth-service`, `content-service`, `media-service`).

Le `front-end` dispose également de son propre nginx dédié pour servir les fichiers statiques (HTML, CSS, JS).

---

## Conséquences

### Avantages

- **Performances** : nginx gère nativement la concurrence avec un modèle event-driven, sans surcoût d'un serveur Python pour le simple routage.
- **Séparation des responsabilités** : nginx gère le transport (TLS, compression, keep-alive), Python gère la logique métier du gateway (authentification, transformation de requêtes).
- **Point d'entrée unique** pour tous les clients : les services internes restent invisibles depuis l'extérieur.
- **Configuration déclarative** : `nginx.conf` est lisible et versionnable.
- **Front-end découplé** : le front-end a son propre nginx, ce qui permet de le déployer et scaler indépendamment du gateway.

### Inconvénients

- **Double couche** : nginx → api-gateway Python → service cible introduit une latence supplémentaire par rapport à un routage nginx direct vers les services.
- **Configuration dupliquée** : les règles de routage existent potentiellement dans `nginx.conf` ET dans `router.py` de l'api-gateway.
- **Débogage** : une requête traverse plusieurs couches (nginx → Python gateway → service), ce qui complexifie le tracing des erreurs.
- **Pas de service mesh** : sans Istio ou Envoy, les fonctionnalités avancées (circuit breaker, retries automatiques, mTLS) doivent être implémentées manuellement.

### Neutrales

- Cette architecture est cohérente avec les patterns d'API Gateway classiques (Kong, AWS API Gateway) et constitue une bonne introduction aux concepts d'infrastructure.

---

## Alternatives considérées

| Option | Raison du rejet |
|--------|-----------------|
| Traefik | Surcharge de configuration pour un contexte dev local |
| Kong | Trop lourd pour un projet pédagogique |
| Routage nginx direct vers services | Perd la couche logique applicative du gateway Python |

---

## Références

- Fichiers de configuration : `api-gateway/nginx.conf`, `front-end/nginx.conf`
- Logique de proxy : `api-gateway/services/proxy.py`, `api-gateway/handlers/gateway.py`
- Routage applicatif : `api-gateway/router.py`