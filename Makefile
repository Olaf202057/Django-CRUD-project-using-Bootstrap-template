.PHONY: all env virtualenv install build build-migrations migrate test

SHELL := /usr/bin/env bash
MYPROJECT_VENV ?= .venv
PYTHON_BIN ?= python

all: env virtualenv install build migrate test

env:
	cp -n .env.example .env | true
	cp -n ansible/group_vars/web.yml.example ansible/group_vars/web.yml | true
	cp -n ansible/hosts/stage.example ansible/hosts/stage | true

virtualenv:
	@if [ ! -d "$(MYPROJECT_VENV)" ]; then \
		$(PYTHON_BIN) -m pip install virtualenv; \
		$(PYTHON_BIN) -m virtualenv $(MYPROJECT_VENV); \
	fi

install: env virtualenv
	@( \
		source $(MYPROJECT_VENV)/bin/activate; \
		python -m pip install -r requirements.txt; \
	)
	@$(PYTHON_BIN) -m pip install "heliumcli>=1.2.2" "ansible>=2.5"

build: virtualenv
	@( \
		source $(MYPROJECT_VENV)/bin/activate; \
		python manage.py collectstatic --noinput; \
	)

build-migrations: env virtualenv install
	@( \
		source $(MYPROJECT_VENV)/bin/activate; \
		python manage.py makemigrations; \
	)

migrate: virtualenv
	@( \
		source $(MYPROJECT_VENV)/bin/activate; \
		python manage.py migrate; \
	)

test: virtualenv
	@if [ ! -f ansible/stage.yml ]; then echo "ansible/stage.yml not found" & exit 1 ; fi
	@if [ ! -f ansible/group_vars/web.yml ]; then echo "ansible/group_vars/web.yml not found" & exit 1 ; fi
	@if [ ! -f ansible/hosts/stage ]; then echo "ansible/hosts/stage not found" & exit 1 ; fi

	@$(PYTHON_BIN) -c "import heliumcli" || (echo "helium-cli not installed"; exit 1)

	@ansible-playbook ansible/stage.yml --syntax-check

	@( \
		source $(MYPROJECT_VENV)/bin/activate; \
		python -m coverage run --source='.' manage.py test && python -m coverage html; \
	)
