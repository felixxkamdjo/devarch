# tests/unit/test_security.py
import pytest
from utils.security import generate_salt, hash_password, verify_password


class TestGenerateSalt:

    def test_retourne_une_chaine(self):
        assert isinstance(generate_salt(), str)

    def test_longueur_par_defaut(self):
        # length=16 bytes → 32 caractères hexadécimaux
        assert len(generate_salt()) == 32

    def test_longueur_personnalisee(self):
        assert len(generate_salt(length=8)) == 16

    def test_deux_sels_sont_differents(self):
        # CRITIQUE : deux sels identiques = faille de sécurité
        assert generate_salt() != generate_salt()

    def test_contient_uniquement_des_caracteres_hex(self):
        assert all(c in "0123456789abcdef" for c in generate_salt())


class TestHashPassword:

    def test_retourne_une_chaine(self):
        assert isinstance(hash_password("motdepasse", "sel"), str)

    def test_hash_different_du_mot_de_passe(self):
        password = "secret123"
        assert hash_password(password, generate_salt()) != password

    def test_meme_entree_meme_sortie(self):
        # Déterminisme : indispensable pour que verify_password fonctionne
        h1 = hash_password("secret123", "sel_fixe")
        h2 = hash_password("secret123", "sel_fixe")
        assert h1 == h2

    def test_sels_differents_donnent_hashes_differents(self):
        assert hash_password("secret123", "sel_A") != hash_password(
            "secret123", "sel_B"
        )

    def test_mots_de_passe_differents_donnent_hashes_differents(self):
        assert hash_password("aaa", "sel") != hash_password("bbb", "sel")

    def test_longueur_hash_sha256(self):
        # SHA256 - toujours 64 caractères hexadécimaux
        assert len(hash_password("anything", "anysalt")) == 64


class TestVerifyPassword:

    def test_mot_de_passe_correct_retourne_true(self):
        salt = generate_salt()
        stored = hash_password("bon_password", salt)
        assert verify_password("bon_password", salt, stored) is True

    def test_mauvais_mot_de_passe_retourne_false(self):
        salt = generate_salt()
        stored = hash_password("bon_password", salt)
        assert verify_password("mauvais_password", salt, stored) is False

    def test_casse_compte(self):
        # "secret" ≠ "Secret" — un seul caractère différent change tout
        salt = generate_salt()
        stored = hash_password("secret", salt)
        assert verify_password("Secret", salt, stored) is False

    def test_mauvais_sel_retourne_false(self):
        stored = hash_password("password", "bon_sel")
        assert verify_password("password", "mauvais_sel", stored) is False

    def test_hash_altere_retourne_false(self):
        salt = generate_salt()
        stored = hash_password("password", salt)
        assert verify_password("password", salt, stored[:-1] + "x") is False

    def test_retourne_un_booleen(self):
        salt = generate_salt()
        stored = hash_password("password", salt)
        assert isinstance(verify_password("password", salt, stored), bool)
