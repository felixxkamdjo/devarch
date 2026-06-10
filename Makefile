# /Makefile

# VARIABLES
COMPOSE=docker compose


# START
up:
	$(COMPOSE) up --build


# START DETACHED
upd:
	$(COMPOSE) up --build -d


# STOP
down:
	$(COMPOSE) down


# RESTART
restart:
	$(COMPOSE) down
	$(COMPOSE) up --build


# LOGS
logs:
	$(COMPOSE) logs -f


# CLEAN
clean:
	docker system prune -f


# REBUILD
rebuild:
	$(COMPOSE) build --no-cache


tree:
	tree -I "venv|__pycache__"

test-short:
	python -m pytest tests/unit/ --tb=short -v 2>&1 | tail -20