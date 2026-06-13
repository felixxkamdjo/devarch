import importlib.util
import os
import sys
import types
from pathlib import Path
from unittest.mock import MagicMock

# Define project and service root paths
project_root = Path(__file__).parent
auth_service_root = project_root / "auth-service"
content_service_root = project_root / "content-service"

# Set default environment variables for testing
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-for-pytest-only")
os.environ.setdefault("DB_PATH", ":memory:")

os.environ.setdefault("RABBITMQ_HOST", "localhost")
os.environ.setdefault("RABBITMQ_USER", "devarch")
os.environ.setdefault("RABBITMQ_PASS", "devarch123")

# Mock external pika dependency
pika_mock = MagicMock()
sys.modules["pika"] = pika_mock
sys.modules["pika.exceptions"] = MagicMock()

# Mock external jwt dependency
jwt_mock = MagicMock()
jwt_mock.encode.return_value = "mocked.jwt.token"
jwt_mock.decode.return_value = {
    "user_id": 1,
    "email": "test@test.com",
    "role": "author",
    "exp": 9999999999,
}
jwt_mock.ExpiredSignatureError = Exception
jwt_mock.InvalidTokenError = Exception
sys.modules["jwt"] = jwt_mock


# Helper to create virtual parent packages in sys.modules
def make_package(name: str, path: Path) -> types.ModuleType:
    pkg = types.ModuleType(name)
    pkg.__path__ = [str(path)]
    pkg.__package__ = name
    sys.modules[name] = pkg
    return pkg


make_package("auth_service", auth_service_root)
make_package("auth_service.utils", auth_service_root / "utils")
make_package("auth_service.services", auth_service_root / "services")
make_package("auth_service.repositories", auth_service_root / "repositories")
make_package("content_service", content_service_root)
make_package("content_service.services", content_service_root / "services")
make_package("content_service.repositories", content_service_root / "repositories")
make_package("content_service.events", content_service_root / "events")


# Helper to dynamically load Python modules and handle circular imports
def load_module(alias: str, file_path: Path) -> types.ModuleType:
    if not file_path.exists():
        raise FileNotFoundError(f"[conftest] Not found: {file_path}")
    spec = importlib.util.spec_from_file_location(alias, file_path)
    module = importlib.util.module_from_spec(spec)
    module.__package__ = alias.rsplit(".", 1)[0] if "." in alias else alias
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


# Initialize auth_service database mocks
auth_db = types.ModuleType("auth_service.db")
auth_db.get_connection = MagicMock(return_value=MagicMock())
sys.modules["auth_service.db"] = auth_db
sys.modules["db"] = auth_db

# Load auth_service modules
load_module("auth_service.utils.security", auth_service_root / "utils/security.py")
load_module("auth_service.utils.jwt", auth_service_root / "utils/jwt.py")

# Bind and expose auth_service utility helpers
auth_utils = sys.modules["auth_service.utils"]
_sec = sys.modules["auth_service.utils.security"]
_jwt = sys.modules["auth_service.utils.jwt"]
auth_utils.generate_salt = _sec.generate_salt
auth_utils.hash_password = _sec.hash_password
auth_utils.verify_password = _sec.verify_password
auth_utils.encode_token = _jwt.encode_token
auth_utils.verify_token = _jwt.verify_token

# Map short aliases for auth_service testing
sys.modules["utils"] = auth_utils
sys.modules["utils.security"] = _sec
sys.modules["utils.jwt"] = _jwt

# Load and map auth_service repositories
load_module(
    "auth_service.repositories.users",
    auth_service_root / "repositories/users.py",
)
auth_repos = sys.modules["auth_service.repositories"]
_users = sys.modules["auth_service.repositories.users"]
auth_repos.create_user = _users.create_user
auth_repos.get_user_by_email = _users.get_user_by_email
auth_repos.get_user_by_id = _users.get_user_by_id
sys.modules["repositories"] = auth_repos

# Load and map auth_service services
load_module("auth_service.services.auth", auth_service_root / "services/auth.py")
auth_services = sys.modules["auth_service.services"]
auth_services.auth = sys.modules["auth_service.services.auth"]
sys.modules["services"] = auth_services
sys.modules["services.auth"] = sys.modules["auth_service.services.auth"]

# Clear temporary short aliases to prevent conflicts with content_service
for short in ["db", "repositories"]:
    sys.modules.pop(short, None)

# Initialize content_service database mocks
content_db = types.ModuleType("content_service.db")
content_db.get_connection = MagicMock(return_value=MagicMock())
sys.modules["content_service.db"] = content_db
sys.modules["db"] = content_db

# Load and map content_service events publisher
load_module(
    "content_service.events.publisher",
    content_service_root / "events/publisher.py",
)
content_events = sys.modules["content_service.events"]
content_events.publisher = sys.modules["content_service.events.publisher"]
sys.modules["events"] = content_events
sys.modules["events.publisher"] = sys.modules["content_service.events.publisher"]

# Load and map content_service repositories
load_module(
    "content_service.repositories.article_repository",
    content_service_root / "repositories/article_repository.py",
)
content_repos = sys.modules["content_service.repositories"]
_art_repo = sys.modules["content_service.repositories.article_repository"]
content_repos.create_article = _art_repo.create_article
content_repos.get_all_articles = _art_repo.get_all_articles
content_repos.get_article_by_id = _art_repo.get_article_by_id
content_repos.update_article = _art_repo.update_article
content_repos.delete_article = _art_repo.delete_article
sys.modules["repositories"] = content_repos
sys.modules["repositories.article_repository"] = _art_repo

# Load and map content_service services
load_module(
    "content_service.services.articles",
    content_service_root / "services/articles.py",
)
content_services = sys.modules["content_service.services"]
content_services.articles = sys.modules["content_service.services.articles"]
sys.modules["services.articles"] = sys.modules["content_service.services.articles"]

# Final cleanup of shared global aliases
for short in ["db", "repositories"]:
    sys.modules.pop(short, None)
