# Makefile for my projects

# This Makefile uses Poetry for dependency management and virtual environments
# It includes targets for installing dependencies, running the app, testing, linting,
# formatting, building executables, cleaning up build artifacts, generating documentation,
# and working with Docker.

# Select which operating system this is running on to set appropriate commands
# OS = Windows_NT
#OS = Unix-Like

##########################################################################################################

MAIN_NOTEBOOK = notebooks/notebook1.ipynb

##########################################################################################################

# Detect OS and set commands accordingly
ifeq ($(OS), Windows_NT)
	SHELL := pwsh.exe -noprofile -command
	RM = Remove-Item -Recurse -Force -Erroraction SilentlyContinue
	MKDIR = mkdir
	SHOW_ENV = @pwsh -noprofile -command "(Get-Command python).source"
	
else # Unix-like OS detected

	SHELL := /bin/bash
	RM = rm -rf
	MKDIR = mkdir -p
	
	SHOW_ENV = which python
endif

# Tool commands
PYTHON = python 

RUN = poetry run # Use 'poetry run' to ensure commands run in the Poetry-managed environment
POETRY = poetry 


# Phony targets
.PHONY: help install venv-activate show-envrun test lint format build clean clean-docs clean-all docker-build docker-run docker-shell

# Default target
help:
	@echo "$(OS) detected"
	@echo ""
	@echo "Usage:"
	@echo "  make install        Install dependencies with Poetry"
	@echo "  make venv-activate  Get instructions to activate the virtual environment"
	@echo "  make show-env       Show current path to the virtual environment's Python interpreter"
	@echo "  make run-notebook   Start VSC with the default notebook"
	@echo ""
	@echo "  make poetry-install Install dependencies with Poetry (Alias for 'make install')"
	@echo "  make poetry-update  Update dependencies with Poetry"
	@echo ""
	@echo "  make git-init       Initialize a new git repository"
	@echo ""
	@echo "  make vsc            Start Visual Studio Code using the current project environment"	
	@echo ""
	@echo "  make requirements   Export dependencies to requirements.txt"

install:
	$(POETRY) install

venv-activate:
ifeq ($(OS), Windows_NT)
	@echo "Run the following command in your PowerShell terminal to activate the virtual environment:"
	@echo ""
	@echo "    Invoke-Expression (poetry env activate)"
	@echo ""
	@echo "Then to show the python executable location:"
	@echo ""
	@echo "    make show-env"
	@echo ""
else
	@echo "Run the following command in your bash (NOT Git Bash) terminal to activate the virtual environment:"
	@echo ""
	@echo "    source `poetry env info --path`/bin/activate"
	@echo ""
	@echo "Then to show the python executable location (to verify correct activation):"
	@echo ""
	@echo "    `which python` or `make show-env`
	@echo ""
endif

	@echo "For instructions on activating in Git Bash, run:"
	@echo ""
	@echo "    make venv-activate-gitbash"
	@echo ""

venv-activate-gitbash:
	@echo "Run the following command in your Git Bash terminal to activate the virtual environment:"
	@echo ""
	@echo "    source `cygpath -u $$(poetry env info --path)/Scripts/activate`"
	@echo ""
	@echo "Then to show the python executable location (to verify correct activation):"
	@echo ""
	@echo "    which python"
	@echo ""

show-env:
	@echo "Virtual environment Python path:"
	@$(SHOW_ENV)
	
# Run the application
run-notebook: # venv-activate
	$(RUN) code -n . $(MAIN_NOTEBOOK)

# poetry targets
poetry-install:
	$(POETRY) install

poetry-update:
	$(POETRY) update
	
# Initialize a new git repository
git-init:
	git init
	git add .
	git commit -m "Initial commit"
	
# Visual Studio Code target
vsc:
	$(RUN) code -n .

# Export requirements.txt - note that this will not include dev dependencies and is mainly for Docker use
# Also note that 'requirements.txt' is in .gitignore to avoid confusion with Poetry's dependency management
requirements:
	$(POETRY) self add poetry-plugin-export@latest
	$(POETRY) export -f requirements.txt --output requirements.txt --without-hashes

FORCE: