# services/auth.py

from repositories import create_user, get_user_by_email, get_user_by_id
from utils import generate_salt, hash_password, verify_password
from utils import encode_token, verify_token


def register_user(user_firstname, user_lastname, email, password):
    """
    Registers a new user.
    """

    if not user_firstname:
        raise ValueError("First name is required.")

    if not user_lastname:
        raise ValueError("Last name is required.")

    if not email:
        raise ValueError("Email is required.")

    if not password:
        raise ValueError("Password is required.")

    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    existing_user = get_user_by_email(email)
    if existing_user:
        raise ValueError("Email already exists.")

    salt = generate_salt()
    password_hash = hash_password(password, salt)

    create_user(
        user_firstname=user_firstname,
        user_lastname=user_lastname,
        email=email,
        password_hash=password_hash,
        salt=salt,
    )

    created_user = get_user_by_email(email)

    return {
        "id": created_user["id"],
        "user_firstname": created_user["user_firstname"],
        "user_lastname": created_user["user_lastname"],
        "email": created_user["email"],
        "role": created_user["role"],
    }


def login_user(email, password):
    """
    Authenticates a user and returns a JWT + user info.
    """

    user = get_user_by_email(email)
    if not user:
        raise ValueError("Invalid credentials.")

    is_valid = verify_password(
        password=password, salt=user["salt"], stored_hash=user["password_hash"]
    )
    if not is_valid:
        raise ValueError("Invalid credentials.")

    # Token avec user_firstname inclus
    token = encode_token(
        user_id=user["id"],
        email=user["email"],
        role=user["role"],
        user_firstname=user["user_firstname"],
        user_lastname=user["user_lastname"],
    )

    return {
        "token": token,
        "user": {
            "id": user["id"],
            "user_firstname": user["user_firstname"],
            "user_lastname": user["user_lastname"],
            "email": user["email"],
            "role": user["role"],
        },
    }


def validate_user_token(token):
    payload = verify_token(token)
    if not payload:
        raise ValueError("Invalid or expired token.")
    return payload


def get_current_user(token):
    payload = validate_user_token(token)
    user = get_user_by_id(payload["user_id"])
    if not user:
        raise ValueError("User not found.")

    return {
        "id": user["id"],
        "user_firstname": user["user_firstname"],
        "user_lastname": user["user_lastname"],
        "email": user["email"],
        "role": user["role"],
    }
