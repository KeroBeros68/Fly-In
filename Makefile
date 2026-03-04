.SILENT:
.ONESHELL:
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

# **************************************************************************** #
#                                   COLORS                                     #
# **************************************************************************** #

GREEN   := \033[0;32m
RED     := \033[0;31m
YELLOW  := \033[0;33m
BLUE    := \033[0;34m
MAGENTA := \033[0;35m
CYAN    := \033[0;36m
RESET   := \033[0m

ECHO    := echo -e

# **************************************************************************** #
#                                  VARIABLES                                   #
# **************************************************************************** #

NAME := main.py
VENV := .venv
PYTHON := $(VENV)/bin/python
INSTALL := uv
INSTALL_CMD := sync
PYTEST := pytest

ARGV :=
SRC_MYPY ?= .

ifeq ($(strip $(SRC_MYPY)),)
$(error SRC_MYPY must not be empty)
endif

# **************************************************************************** #
#									.PHONY									   #
# **************************************************************************** #

.PHONY: install run debug lint lint-strict clean fclean \
		st add _commit push_feat push_fix push_refactor \
		push_docs push_style push_chore test

# **************************************************************************** #
#									Help									   #
# **************************************************************************** #


help:
	$(ECHO) "$(YELLOW)Available commands:$(RESET)"
	$(ECHO) ""
	$(ECHO) "$(CYAN)  📦 Setup$(RESET)"
	$(ECHO) "  make install              Install dependencies with $(INSTALL)"
	$(ECHO) ""
	$(ECHO) "$(CYAN)  🚀 Run$(RESET)"
	$(ECHO) "  make run [ARGV=...]       Run the project (optional args)"
	$(ECHO) "  make debug [ARGV=...]     Run the project with pdb debugger"
	$(ECHO) ""
	$(ECHO) "$(CYAN)  🧪 Tests$(RESET)"
	$(ECHO) "  make test                 Run tests with $(PYTEST)"
	$(ECHO) ""
	$(ECHO) "$(CYAN)  🔍 Lint$(RESET)"
	$(ECHO) "  make lint                 Run flake8 + mypy"
	$(ECHO) "  make lint-strict          Run flake8 + mypy (strict mode)"
	$(ECHO) ""
	$(ECHO) "$(CYAN)  🧹 Clean$(RESET)"
	$(ECHO) "  make clean                Remove __pycache__ and .mypy_cache"
	$(ECHO) "  make fclean               clean + remove app.log"
	$(ECHO) ""
	$(ECHO) "$(CYAN)  🔧 Git$(RESET)"
	$(ECHO) "  make st                   git status"
	$(ECHO) "  make add                  git add all files"
	$(ECHO) "  make push_feat M='...'    Commit + push (type: feat)"
	$(ECHO) "  make push_fix M='...'     Commit + push (type: fix)"
	$(ECHO) "  make push_refactor M='...' Commit + push (type: refactor)"
	$(ECHO) "  make push_docs M='...'    Commit + push (type: docs)"
	$(ECHO) "  make push_style M='...'   Commit + push (type: style)"
	$(ECHO) "  make push_chore M='...'   Commit + push (type: chore)"

# **************************************************************************** #
#									Rules									   #
# **************************************************************************** #

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(ECHO) -n "${CYAN}Checking $(INSTALL)...${RESET} ";
	if command -v $(INSTALL) > /dev/null 2>&1; then
		$(ECHO) "${GREEN}✓ $(INSTALL) is installed${RESET}";
	else
		$(ECHO) "${YELLOW}⚠ $(INSTALL) not found${RESET}";
		$(ECHO) -n "${CYAN}Installing $(INSTALL)...${RESET} ";
		if python3 -m pip install --user --upgrade $(INSTALL) > /dev/null 2>&1; then
			$(ECHO) "${GREEN}✓${RESET}";
		else
			$(ECHO) "${RED}✗ Failed to install $(INSTALL)${RESET}";
			exit 1;
		fi;
	fi;
	$(ECHO) -n "${CYAN}Installing dependencies with $(INSTALL)...${RESET} ";
	if $(INSTALL) $(INSTALL_CMD) > /dev/null 2>&1; then
		$(ECHO) "${GREEN}✓${RESET}";
	else \
		$(ECHO) "${RED}✗${RESET}";
		$(INSTALL) $(INSTALL_CMD);
	fi;
	$(INSTALL) add --dev flake8 mypy pytest
	$(ECHO) "${GREEN}✓ Installation complete${RESET}";

run: $(VENV)
	$(PYTHON) $(NAME) $(ARGV)

debug: $(VENV)
	$(PYTHON) -m pdb $(NAME) $(ARGV)

lint: $(VENV)
	$(ECHO) "${CYAN}Running flake8...${RESET}";
	$(PYTHON) -m flake8 --exclude=matrix_env;
	$(ECHO) "${CYAN}Running mypy...${RESET}";
	$(PYTHON) -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude=matrix_env $(SRC_MYPY)

lint-strict: $(VENV)
	$(PYTHON) -m flake8 --exclude=matrix_env
	$(PYTHON) -m mypy --strict --exclude=matrix_env $(SRC_MYPY)

clean:
	printf "$(CYAN)Suppression de __pycache__...$(RESET) "
	if find . -type d -name "__pycache__" | grep -q .; then
		find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null;
		$(ECHO) "$(GREEN)✓ Dossiers __pycache__ supprimés$(RESET)";
	else
		$(ECHO) "$(YELLOW)⚠ Rien à nettoyer$(RESET)";
	fi
	printf "$(CYAN)Suppression de .mypy_cache...$(RESET) "
	if find . -type d -name ".mypy_cache" | grep -q .; then
		find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null;
		$(ECHO) "$(GREEN)✓ Dossiers .mypy_cache supprimés$(RESET)";
	else
		$(ECHO) "$(YELLOW)⚠ Rien à nettoyer$(RESET)";
	fi

fclean: clean
	printf "$(CYAN)Suppression de app.log...$(RESET) "
	if find . -name "app.log" -type f | grep -q .; then
		find . -name "app.log" -type f -exec rm -f {} + 2>/dev/null;
		$(ECHO) "$(GREEN)✓ Fichier app.log supprimé$(RESET)";
	else
		$(ECHO) "$(YELLOW)⚠ Rien à nettoyer$(RESET)";
	fi

test: $(VENV)
	$(ECHO) "$(GREEN)Running tests...$(RESET)"
	$(PYTHON) -m $(PYTEST)

st:
	git status

add:
	$(ECHO) "$(CYAN)--- Status ---$(RESET)"
	git status -s
	git add .
	$(ECHO) "$(GREEN)✔ Files added.$(RESET)"
	git status -s
	$(ECHO) "$(GREEN)✔ Done$(RESET)\n"

_commit: add
	BRANCH=$$(git branch --show-current);
	if [ -z "$(M)" ]; then
		$(ECHO) "$(RED)Error: Le message du commit (M) est vide !$(RESET)";
		exit 1;
	fi
	git commit -m "$(TYPE): $(M)"
	git push --set-upstream origin $(BRANCH)
	$(ECHO) "$(GREEN)🚀 Successful push ($(TYPE)).$(RESET)\n"

push_feat:
	$(MAKE) _commit TYPE=feat M="$(M)"

push_fix:
	$(MAKE) _commit TYPE=fix M="$(M)"

push_refactor:
	$(MAKE) _commit TYPE=refactor M="$(M)"

push_docs:
	$(MAKE) _commit TYPE=docs M="$(M)"

push_style:
	$(MAKE) _commit TYPE=style M="$(M)"

push_chore:
	$(MAKE) _commit TYPE=chore M="$(M)"
