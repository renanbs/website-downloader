.DEFAULT_GOAL := default_target

PROJECT_NAME := website_downloader
PYTHON_VERSION := 3.8.3
VENV_NAME := $(PROJECT_NAME)-$(PYTHON_VERSION)

setup-dev:
	pip install pip --upgrade
	pip install -U setuptools
	pip install -r requirements-dev.txt

.create-venv:
	pyenv install -s $(PYTHON_VERSION)
	pyenv uninstall -f $(VENV_NAME)
	pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME)
	pyenv local $(VENV_NAME)

create-venv: .create-venv setup-dev

.clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr reports/
	rm -fr .pytest_cache/
	rm -f coverage.xml

clean: .clean-build .clean-pyc .clean-test ## remove all build, test, coverage and Python artifacts

pycodestyle:
	echo "Running pycodestyle"
	pycodestyle

flake8:
	echo "Running flake8"
	flake8

pylint:
	# "Running pylint"
	#pylint

code-convention: pycodestyle flake8

test:
	# "Running unit tests"
	pytest -v --cov-report=term-missing --cov-report=html --cov-report=xml --cov=website_downloader --cov-fail-under=80

default_target: clean code-convention test
