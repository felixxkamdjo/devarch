# ADR-001 - Utilisation exclusive de la stdlib Python pour les services backend

| Champ       | Valeur                        |
|-------------|-------------------------------|
| **Date**    | 2025-05-01                    |
| **Statut**  | Accepté                       |
| **Auteurs** | Équipe devarch                |

---

## Contexte

Le projet devarch est une plateforme de blog headless construite en architecture microservices. Chaque service backend (`auth-service`, `content-service`, `media-service`, `consumer-service`) est développé en Python 3.13. Au moment du démarrage du projet, l'équipe devait choisir entre plusieurs approches pour l'implémentation des serveurs HTTP :

- **Option A** : Frameworks web tiers (FastAPI, Flask, Django REST Framework)
- **Option B** : Stdlib Python uniquement (`http.server`, `socketserver`, modules standards)

La contrainte principale était pédagogique et de maîtrise : comprendre en profondeur le fonctionnement d'un serveur HTTP avant d'utiliser des abstractions de haut niveau.

---

## Décision

**Utiliser exclusivement la bibliothèque standard Python (stdlib) pour tous les services backend**, sans aucune dépendance externe pour la couche HTTP et le routage.

Chaque service implémente son propre serveur via `http.server.BaseHTTPRequestHandler`, avec un routeur maison (`router.py`) et des utilitaires partagés (`utils/http.py`) pour la sérialisation JSON et la gestion des réponses.

---

## Conséquences

### Avantages

- **Zéro dépendance externe** pour la couche serveur : images Docker plus légères, pas de CVE liées à des frameworks tiers.
- **Compréhension profonde** du cycle requête/réponse HTTP (parsing des headers, body, méthodes).
- **Uniformité** : chaque service suit exactement la même structure (`server.py` → `router.py` → `handlers/` → `services/` → `repositories/`).
- **Contrôle total** sur le comportement du serveur sans magie cachée.

### Inconvénients

- **Code boilerplate** répété dans chaque service (routage, parsing JSON, gestion des erreurs HTTP).
- **Absence de fonctionnalités avancées** out-of-the-box : validation de schéma, serialisation automatique, middleware standardisé, documentation OpenAPI auto-générée.
- **Effort de maintenance** accru si les besoins évoluent (ex. : ajout de WebSockets, streaming).
- **Courbe d'apprentissage inversée** : les développeurs juniors arrivant sur le projet doivent apprendre la convention maison avant d'être productifs.

### Neutrales

- Cette décision est **intentionnellement temporaire** dans un contexte de stage/apprentissage. En production réelle, un framework comme FastAPI serait justifié dès le départ.

---

## Alternatives considérées

| Option | Raison du rejet |
|--------|-----------------|
| FastAPI | Trop d'abstraction pour l'objectif pédagogique initial |
| Flask | Dépendance externe, même légère, jugée superflue pour ce contexte |
| aiohttp | Introduit la complexité de l'async sans bénéfice immédiat |

---

## Références

- Structure commune observée dans : `auth-service/server.py`, `content-service/server.py`, `media-service/server.py`
- Pattern de routage : `*/router.py` dans chaque service