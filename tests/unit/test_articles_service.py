# tests/unit/test_articles_service.py
import pytest
from unittest.mock import patch
from services.articles import (
    create_article_service, get_article_service,
    update_article_service, delete_article_service
)

ARTICLES_SVC = "content_service.services.articles"


class TestCreateArticleServiceValidations:

    def test_titre_vide_leve_valueerror(self):
        with patch(f"{ARTICLES_SVC}.create_article"), patch(f"{ARTICLES_SVC}.publish"):
            with pytest.raises(ValueError, match="Title is required"):
                create_article_service("", "Contenu valide", author_id=1)

    def test_titre_espaces_seulement_leve_valueerror(self):
        with patch(f"{ARTICLES_SVC}.create_article"), patch(f"{ARTICLES_SVC}.publish"):
            with pytest.raises(ValueError, match="Title is required"):
                create_article_service("   ", "Contenu valide", author_id=1)

    def test_contenu_vide_leve_valueerror(self):
        with patch(f"{ARTICLES_SVC}.create_article"), patch(f"{ARTICLES_SVC}.publish"):
            with pytest.raises(ValueError, match="Content is required"):
                create_article_service("Titre valide", "", author_id=1)

    def test_author_id_none_leve_valueerror(self):
        with patch(f"{ARTICLES_SVC}.create_article"), patch(f"{ARTICLES_SVC}.publish"):
            with pytest.raises(ValueError, match="author_id is required"):
                create_article_service("Titre", "Contenu", author_id=None)


class TestCreateArticleServiceHappyPath:

    def test_retourne_article_id(self):
        with patch(f"{ARTICLES_SVC}.create_article", return_value=42) as mock_create, \
             patch(f"{ARTICLES_SVC}.publish"):
            result = create_article_service("Mon article", "Contenu", author_id=1)
        assert result == 42

    def test_titre_strip_avant_sauvegarde(self):
        # Avoid space issues
        with patch(f"{ARTICLES_SVC}.create_article", return_value=1) as mock_create, \
             patch(f"{ARTICLES_SVC}.publish"):
            create_article_service("  Mon article  ", "Contenu", author_id=1)
        args = mock_create.call_args[1]
        assert args["title"] == "Mon article"

    def test_status_draft_par_defaut(self):
        with patch(f"{ARTICLES_SVC}.create_article", return_value=1) as mock_create, \
             patch(f"{ARTICLES_SVC}.publish"):
            create_article_service("Titre", "Contenu", author_id=1)
        assert mock_create.call_args[1]["status"] == "draft"

    def test_publish_appele_apres_creation(self):
        with patch(f"{ARTICLES_SVC}.create_article", return_value=5), \
             patch(f"{ARTICLES_SVC}.publish") as mock_publish:
            create_article_service("Titre", "Contenu", author_id=1, author_name="Felix")
        mock_publish.assert_called_once_with(
            "article.published",
            {"article_id": 5, "title": "Titre",
             "author_id": 1, "author_name": "Felix"}
        )

    def test_author_name_none_devient_chaine_vide(self):
        # Convert None to empty string to avoid issues in publish payload
        with patch(f"{ARTICLES_SVC}.create_article", return_value=1), \
             patch(f"{ARTICLES_SVC}.publish") as mock_publish:
            create_article_service("Titre", "Contenu", author_id=1, author_name=None)
        payload = mock_publish.call_args[0][1]
        assert payload["author_name"] == ""


class TestGetArticleService:

    def test_article_inexistant_leve_valueerror(self):
        with patch(f"{ARTICLES_SVC}.get_article_by_id", return_value=None):
            with pytest.raises(ValueError, match="Article not found"):
                get_article_service(9999)

    def test_article_existant_retourne_dict(self):
        faux_article = {"id": 1, "title": "Test", "content": "Contenu",
                        "author_id": 1, "status": "published"}
        with patch(f"{ARTICLES_SVC}.get_article_by_id", return_value=faux_article):
            result = get_article_service(1)
        assert result["id"] == 1
        assert result["title"] == "Test"


class TestUpdateArticleService:

    def test_titre_vide_leve_valueerror(self):
        with patch(f"{ARTICLES_SVC}.update_article"):
            with pytest.raises(ValueError, match="Title and content are required"):
                update_article_service(1, "", "Contenu", "published")

    def test_contenu_vide_leve_valueerror(self):
        with patch(f"{ARTICLES_SVC}.update_article"):
            with pytest.raises(ValueError, match="Title and content are required"):
                update_article_service(1, "Titre", "", "published")

    def test_update_valide_appelle_repository(self):
        with patch(f"{ARTICLES_SVC}.update_article") as mock_update:
            update_article_service(1, "Titre", "Contenu", "published")
        mock_update.assert_called_once()


class TestDeleteArticleService:

    def test_delete_appelle_repository_avec_bon_id(self):
        with patch(f"{ARTICLES_SVC}.get_article_by_id", return_value={"id": 7, "author_id": 1}) as mock_get, \
            patch(f"{ARTICLES_SVC}.delete_article") as mock_delete:
            delete_article_service(
                article_id=7,
                requesting_user_id=1,
                requesting_user_role="admin"
            )
        mock_delete.assert_called_once_with(7)