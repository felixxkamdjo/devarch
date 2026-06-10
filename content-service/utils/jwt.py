# auth/jwt.py

import time
import jwt


# Secret key used to sign tokens
SECRET_KEY = "my-super-secret-key"

# JWT algorithm
ALGORITHM = "HS256"

# Token expiration duration
TOKEN_EXPIRATION = 3600  # 1 hour


def encode_token(user_id, email, role):
    """
    Generates a JWT token.
    """

    payload = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "exp": int(time.time()) + TOKEN_EXPIRATION
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def decode_token(token):
    """
    Decodes the JWT payload without verification.
    """

    payload = jwt.decode(
        token,
        options={"verify_signature": False}
    )

    return payload


def verify_token(token):
    """
    Verifies token signature and expiration.
    Returns the decoded payload if valid.
    """

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        return payload

    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None

    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None