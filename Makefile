# =========================================
# Project configuration
# =========================================
UV          := uv
PYTHON      := $(UV) run python
PRECOMMIT   := $(UV) run pre-commit
PYTEST      := $(UV) run pytest
MKDOCS      := $(UV) run mkdocs
PIPAUDIT    := $(UV) run pip-audit
BANDIT      := $(UV) run bandit
DOCKER      := docker compose

SRC := app
TESTS := app/tests


# =========================================
# Help
# =========================================
.PHONY: help
help:
	@echo "========== Setup =========="
	@echo "make install        Install all dependencies"
	@echo "make env            Generate .env with secure random values"
	@echo "make init           Full init: env + install + docker"
	@echo ""
	@echo "========== Docker =========="
	@echo "make up             Start all services (dev)"
	@echo "make down           Stop all services"
	@echo "make logs           Follow logs"
	@echo "make ps             Show running services"
	@echo ""
	@echo "========== Quality =========="
	@echo "make lint           Run ruff + format"
	@echo "make typecheck      Run mypy"
	@echo "make test           Run pytest"
	@echo "make coverage       HTML coverage report"
	@echo "test-docker         Run pytest in docker"
	@echo "test-docker-cov     Run pytest in docker with coverage"
	@echo ""
	@echo "========== Security =========="
	@echo "make bandit         Code security scan"
	@echo "make security       Dependency audit"
	@echo ""
	@echo "========== Clean =========="
	@echo "make clean          Clean project"
# =========================================
# Setup
# =========================================
.PHONY: install
install:
	$(UV) sync --all-groups
	$(PRECOMMIT) install
	@echo "✅  les dépendances et pre-commit sont installés avec succées"

.PHONY: env
env:
	@$(MAKE) _generate_env
	@echo "✅ .env generated"

.PHONY: _generate_env
_generate_env:
	cat .env.example \
		> .env

.PHONY: init
init:
	@echo "🚀 Initializing project..."
	@if [ ! -f .env ]; then \
		$(MAKE) env; \
	else \
		echo "ℹ️  .env already exists, skipping generation"; \
	fi
	$(MAKE) install
	@echo ""
	@echo "✅✅✅"
	@echo ""
# =========================================
# Docker
# =========================================
.PHONY: up
up:
	$(DOCKER) up -d --build
	@echo "🚀 Building and starting services..."
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  ✅  Services started successfully!"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  ⏳ Opening browser in 3 seconds..."
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@sleep 5
	@if [ "$$(uname)" = "Darwin" ]; then \
		open http://localhost:8000/docs; \
	elif [ "$$(uname)" = "Linux" ]; then \
		xdg-open http://localhost:8000/docs 2>/dev/null || sensible-browser http://localhost:8000/docs; \
	else \
		start http://localhost:8000/docs; \
	fi
	@echo "  🌐 Browser opened → http://localhost:8000/docs"

.PHONY: down
down:
	$(DOCKER) down
	@echo "✅ Services stopped"

.PHONY: logs
logs:
	$(DOCKER) logs -f app

.PHONY: ps
ps:
	$(DOCKER) ps

.PHONY: restart
restart:
	$(DOCKER) restart app
	@echo "✅ App restarted"

# =========================================
# Quality
# =========================================
.PHONY: lint
lint:
	$(PRECOMMIT) run ruff --all-files
	$(PRECOMMIT) run ruff-format --all-files

.PHONY: typecheck
typecheck:
	$(PRECOMMIT) run mypy --all-files

.PHONY: test
test:
	$(PYTEST) --cov=$(SRC) --cov-report=term-missing

.PHONY: coverage
coverage:
	$(PYTEST) --cov=$(SRC) --cov-report=html
	@echo "Coverage report → htmlcov/index.html"
	@if [ "$$(uname)" = "Darwin" ]; then open htmlcov/index.html; \
	elif [ "$$(uname)" = "Linux" ]; then xdg-open htmlcov/index.html; \
	else start htmlcov/index.html; fi

.PHONY: test-docker
test-docker:
	$(DOCKER) run --rm  app uv run pytest app/tests --cov=app --cov-report=term-missing

.PHONY: test-docker-cov
test-docker-cov:
	$(DOCKER) run --rm -v $(PWD)/htmlcov:/app/htmlcov app uv run pytest app/tests --cov=app --cov-report=html
	@echo "Coverage report → htmlcov/index.html"
	@if [ "$$(uname)" = "Darwin" ]; then open htmlcov/index.html; \
	elif [ "$$(uname)" = "Linux" ]; then xdg-open htmlcov/index.html; \
	else start htmlcov/index.html; fi

# Security
# =========================================
.PHONY: bandit
bandit:
	$(BANDIT) -q -r $(SRC) -x $(TESTS)

.PHONY: security
security:
	$(PIPAUDIT) --strict
# =========================================
# Master pipeline
# =========================================
.PHONY: check
check: lint typecheck bandit security test
	@echo "✅✅✅✅"

# =========================================
# Cleaning
# =========================================
.PHONY: clean
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf site
	rm -rf dist
	rm -rf build
	rm -rf .cache/pre-commit
