# tests/unit/test_auth_service.py
import pytest
from unittest.mock import patch
from utils.security import hash_password

# Les fonctions à tester
from services.auth import register_user, login_user, validate_user_token

# Préfixe exact à patcher : le chemin où les fonctions sont UTILISÉES
# (dans auth_service.services.auth), pas là où elles sont définies.
AUTH_SVC = "auth_service.services.auth"

FAUX_USER_BASE = {
    "id": 1, "user_firstname": "Felix", "user_lastname": "Kamdjo",
    "email": "felix@devarch.io", "role": "author",
    "salt": "sel_fixe", "password_hash": hash_password("password123", "sel_fixe")
}


class TestRegisterUserValidations:

    def test_prenom_vide_leve_valueerror(self):
        with patch(f"{AUTH_SVC}.get_user_by_email", return_value=None):
            with patch(f"{AUTH_SVC}.create_user"):
                with pytest.raises(ValueError, match="First name is required"):
                    register_user("", "Kamdjo", "felix@devarch.io", "password123")

    def test_nom_vide_leve_valueerror(self):
        with patch(f"{AUTH_SVC}.get_user_by_email", return_value=None):
            with patch(f"{AUTH_SVC}.create_user"):
                with pytest.raises(ValueError, match="Last name is required"):
                    register_user("Felix", "", "felix@devarch.io", "password123")

    def test_email_vide_leve_valueerror(self):
        with patch(f"{AUTH_SVC}.get_user_by_email", return_value=None):
            with patch(f"{AUTH_SVC}.create_user"):
                with pytest.raises(ValueError, match="Email is required"):
                    register_user("Felix", "Kamdjo", "", "password123")

    def test_password_vide_leve_valueerror(self):
        with patch(f"{AUTH_SVC}.get_user_by_email", return_value=None):
            with patch(f"{AUTH_SVC}.create_user"):
                with pytest.raises(ValueError, match="Password is required"):
                    register_user("Felix", "Kamdjo", "felix@devarch.io", "")

    def test_password_trop_court_leve_valueerror(self):
        with patch(f"{AUTH_SVC}.get_user_by_email", return_value=None):
            with patch(f"{AUTH_SVC}.create_user"):
                with pytest.raises(ValueError, match="at least 8 characters"):
                    register_user("Felix", "Kamdjo", "felix@devarch.io", "abc")

    def test_email_deja_existant_leve_valueerror(self):
        with patch(f"{AUTH_SVC}.get_user_by_email", return_value=FAUX_USER_BASE):
            with pytest.raises(ValueError, match="Email already exists"):
                register_user("Felix", "Kamdjo", "felix@devarch.io", "password123")


class TestLoginUser:

    def test_email_inexistant_leve_valueerror(self):
        with patch(f"{AUTH_SVC}.get_user_by_email", return_value=None):
            with pytest.raises(ValueError, match="Invalid credentials"):
                login_user("inconnu@devarch.io", "password123")

    def test_mauvais_password_leve_valueerror(self):
        with patch(f"{AUTH_SVC}.get_user_by_email", return_value=FAUX_USER_BASE):
            with pytest.raises(ValueError, match="Invalid credentials"):
                login_user("felix@devarch.io", "mauvais_password")

    def test_credentials_corrects_retourne_token_et_user(self):
        with patch(f"{AUTH_SVC}.get_user_by_email", return_value=FAUX_USER_BASE):
            result = login_user("felix@devarch.io", "password123")
        assert "token" in result
        assert "user" in result

    def test_token_est_un_jwt(self):
        with patch(f"{AUTH_SVC}.get_user_by_email", return_value=FAUX_USER_BASE):
            result = login_user("felix@devarch.io", "password123")
        assert len(result["token"].split(".")) == 3

    def test_reponse_sans_donnees_sensibles(self):
        # CRITIQUE : password_hash et salt ne doivent jamais
        # être renvoyés au client
        with patch(f"{AUTH_SVC}.get_user_by_email", return_value=FAUX_USER_BASE):
            result = login_user("felix@devarch.io", "password123")
        user = result["user"]
        assert "password_hash" not in user
        assert "salt" not in user

    def test_user_contient_les_bons_champs(self):
        with patch(f"{AUTH_SVC}.get_user_by_email", return_value=FAUX_USER_BASE):
            result = login_user("felix@devarch.io", "password123")
        assert result["user"]["id"] == 1
        assert result["user"]["role"] == "author"
        assert result["user"]["email"] == "felix@devarch.io"


class TestValidateUserToken:

    def test_token_valide_retourne_payload(self):
        from utils.jwt import encode_token
        token = encode_token(1, "felix@devarch.io", "author")
        result = validate_user_token(token)
        assert result["user_id"] == 1

    def test_token_invalide_leve_valueerror(self):
        with patch("auth_service.services.auth.verify_token", return_value=None):
            with pytest.raises(ValueError, match=r"Invalid or expired token\."):
                validate_user_token("pas_un_token")