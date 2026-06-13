# auth/utils/jwt.py
import os
import time
import jwt

SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXPIRATION = 3600  # 1 heure

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY manquante dans les variables d'environnement")


def encode_token(user_id, email, role, user_firstname="", user_lastname=""):
    """
    Génère un JWT avec l'identité complète de l'utilisateur.
    user_firstname et user_lastname permettent aux autres services
    (content-service) de stocker author_name sans appeler auth-service.
    """
    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "user_firstname": user_firstname,
        "user_lastname": user_lastname,
        "exp": int(time.time()) + TOKEN_EXPIRATION,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token):
    """Décode sans vérification de signature."""
    return jwt.decode(token, options={"verify_signature": False})


def verify_token(token):
    """Vérifie signature et expiration. Retourne le payload ou None."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        print("Token expired.")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None
