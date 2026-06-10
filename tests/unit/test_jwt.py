# tests/unit/test_jwt.py
import time
import pytest
from auth_service.utils.jwt import encode_token, decode_token, verify_token


@pytest.fixture
def token_valide():
    return encode_token(
        user_id=1, email="felix@devarch.io",
        role="author", user_firstname="Felix", user_lastname="Kamdjo"
    )


class TestEncodeToken:

    def test_retourne_une_chaine(self, token_valide):
        assert isinstance(token_valide, str)

    def test_format_jwt_trois_parties(self, token_valide):
        assert len(token_valide.split(".")) == 3

    def test_payload_contient_user_id(self, token_valide):
        assert decode_token(token_valide)["user_id"] == 1

    def test_payload_contient_email(self, token_valide):
        assert decode_token(token_valide)["email"] == "felix@devarch.io"

    def test_payload_contient_role(self, token_valide):
        assert decode_token(token_valide)["role"] == "author"

    def test_payload_contient_user_firstname(self, token_valide):
        assert decode_token(token_valide)["user_firstname"] == "Felix"

    def test_payload_contient_exp(self, token_valide):
        # Sans exp, le token ne expire jamais → faille de sécurité
        assert "exp" in decode_token(token_valide)

    def test_exp_dans_le_futur(self, token_valide):
        assert decode_token(token_valide)["exp"] > int(time.time())

    def test_deux_users_ont_tokens_differents(self):
        t1 = encode_token(1, "user1@test.io", "author")
        t2 = encode_token(2, "user2@test.io", "admin")
        assert t1 != t2


class TestDecodeToken:

    def test_retourne_un_dict(self, token_valide):
        assert isinstance(decode_token(token_valide), dict)

    def test_retrouve_les_donnees_encodees(self, token_valide):
        payload = decode_token(token_valide)
        assert payload["user_id"] == 1
        assert payload["email"] == "felix@devarch.io"


class TestVerifyToken:

    def test_token_valide_retourne_payload(self, token_valide):
        result = verify_token(token_valide)
        assert result is not None
        assert result["user_id"] == 1

    def test_token_expire_retourne_none(self):
        import jwt as pyjwt
        expired = pyjwt.encode(
            {"user_id": 1, "email": "x@x.io", "role": "author",
             "user_firstname": "", "user_lastname": "",
             "exp": int(time.time()) - 10},
            "my-super-secret-key", algorithm="HS256"
        )
        assert verify_token(expired) is None

    def test_token_fausse_signature_retourne_none(self):
        import jwt as pyjwt
        forged = pyjwt.encode(
            {"user_id": 999, "role": "admin", "exp": int(time.time()) + 3600},
            "fausse_cle", algorithm="HS256"
        )
        assert verify_token(forged) is None

    def test_token_invalide_retourne_none(self):
        assert verify_token("pas_un_token") is None

    def test_token_vide_retourne_none(self):
        assert verify_token("") is None