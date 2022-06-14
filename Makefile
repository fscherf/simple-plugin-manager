SHELL=/bin/bash
PYTHON=python3

PYTHON_ENV_ROOT=envs
PYTHON_DEVELOPMENT_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-development-env
PYTHON_TESTING_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-testing-env
PYTHON_PACKAGING_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-packaging-env

.PHONY: clean doc sdist test ci-test lint shell freeze

# environments ################################################################
# development
$(PYTHON_DEVELOPMENT_ENV)/.created: REQUIREMENTS.development.txt
	rm -rf $(PYTHON_DEVELOPMENT_ENV) && \
	$(PYTHON) -m venv $(PYTHON_DEVELOPMENT_ENV) && \
	. $(PYTHON_DEVELOPMENT_ENV)/bin/activate && \
	pip install pip --upgrade && \
	pip install -r ./REQUIREMENTS.development.txt && \
	date > $(PYTHON_DEVELOPMENT_ENV)/.created

dev-env: $(PYTHON_DEVELOPMENT_ENV)/.created

# testing
$(PYTHON_TESTING_ENV)/.created: REQUIREMENTS.testing.txt
	rm -rf $(PYTHON_TESTING_ENV) && \
	$(PYTHON) -m venv $(PYTHON_TESTING_ENV) && \
	. $(PYTHON_TESTING_ENV)/bin/activate && \
	pip install pip --upgrade && \
	pip install -r ./REQUIREMENTS.testing.txt && \
	date > $(PYTHON_TESTING_ENV)/.created

testing-env: $(PYTHON_TESTING_ENV)/.created

# packaging
$(PYTHON_PACKAGING_ENV)/.created: REQUIREMENTS.packaging.txt
	rm -rf $(PYTHON_PACKAGING_ENV) && \
	$(PYTHON) -m venv $(PYTHON_PACKAGING_ENV) && \
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	pip install --upgrade pip && \
	pip install -r REQUIREMENTS.packaging.txt
	date > $(PYTHON_PACKAGING_ENV)/.created

packaging-env: $(PYTHON_PACKAGING_ENV)/.created

# helper
clean:
	rm -rf $(PYTHON_ENV_ROOT)

shell: dev-env
	. $(PYTHON_DEVELOPMENT_ENV)/bin/activate && \
	rlpython

freeze: dev-env
	. $(PYTHON_DEVELOPMENT_ENV)/bin/activate && \
	pip freeze

# tests #######################################################################
test: testing-env
	. $(PYTHON_TESTING_ENV)/bin/activate && \
	rm -rf htmlcov && \
	time tox $(args)

ci-test: testing-env
	. $(PYTHON_TESTING_ENV)/bin/activate && \
	rm -rf htmlcov && \
	time JENKINS_URL=1 tox -r $(args)

# linting #####################################################################
lint: testing-env
	. $(PYTHON_TESTING_ENV)/bin/activate && \
	time tox -e lint

# packaging ###################################################################
sdist: packaging-env
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	rm -rf dist *.egg-info && \
	./setup.py sdist

_release: sdist
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	twine upload --config-file ~/.pypirc.fscherf dist/*
