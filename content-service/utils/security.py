# utils/security.py

import secrets
import hashlib
import hmac


def generate_salt(length=16):
    """
    Generates a cryptographically secure random salt.
    Returns a hexadecimal string.
    """

    return secrets.token_hex(length)


def hash_password(password, salt):
    """
    Hashes a password using SHA256 and a salt.
    Returns a hexadecimal hash string.
    """

    password_and_salt = f"{password}{salt}"

    password_bytes = password_and_salt.encode("utf-8")

    password_hash = hashlib.sha256(password_bytes).hexdigest()

    return password_hash


def verify_password(password, salt, stored_hash):
    """
    Verifies whether a password matches the stored hash.
    """

    computed_hash = hash_password(password, salt)

    return hmac.compare_digest(computed_hash, stored_hash)