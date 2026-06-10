# auth/repositories/users.py

from db import get_connection


def create_user(user_firstname, user_lastname, email,
                password_hash, salt, role="author"):
    """
    Inserts a new user into the database.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO users (
        user_firstname,
        user_lastname,
        email,
        password_hash,
        salt,
        role
    )
    VALUES (?, ?, ?, ?, ?, ?);
    """

    cursor.execute(query, (
        user_firstname,
        user_lastname,
        email,
        password_hash,
        salt,
        role
    ))

    connection.commit()
    connection.close()


def get_user_by_email(email):
    """
    Retrieves a user by email.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT * FROM users
    WHERE email = ?;
    """

    cursor.execute(query, (email,))
    row = cursor.fetchone()
    user = dict(row) if row else None

    connection.close()

    return user


def get_user_by_id(user_id):
    """
    Retrieves a user by ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT * FROM users
    WHERE id = ?;
    """

    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    user = dict(row) if row else None

    connection.close()

    return user


def get_users():
    """
    Retrieves all users.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT * FROM users;
    """

    cursor.execute(query)
    users = [dict(row) for row in cursor.fetchall()]

    connection.close()

    return users


def update_user(user_id, user_firstname,
                user_lastname, email, role):
    """
    Updates user information.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE users
    SET
        user_firstname = ?,
        user_lastname = ?,
        email = ?,
        role = ?
    WHERE id = ?;
    """

    cursor.execute(query, (
        user_firstname,
        user_lastname,
        email,
        role,
        user_id
    ))

    connection.commit()
    connection.close()
    
    
def delete_user(user_id):
    """
    Deletes a user by ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    DELETE FROM users
    WHERE id = ?;
    """

    cursor.execute(query, (user_id,))

    connection.commit()

    connection.close()