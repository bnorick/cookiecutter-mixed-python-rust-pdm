PACKAGE := {{ cookiecutter.package_name }}
PACKAGE_DIR := src/python/${PACKAGE}
MODULES := $(wildcard $(PACKAGE_DIR)/*.py)

# MAIN TASKS ##################################################################

.PHONY: all
all: doctor format check test mkdocs ## Run all tasks that determine CI status

.PHONY: dev
dev: install  ## Continuously run all CI tasks when files chanage
	pdm run ptw

.PHONY: shell
shell: install
	pdm run ipython --ipython-dir=notebooks

.PHONY: demo
demo: install
	pdm run nbstripout notebooks/*.ipynb
	pdm run jupyter notebook --notebook-dir=notebooks --browser=firefox

# SYSTEM DEPENDENCIES #########################################################

.PHONY: bootstrap
bootstrap: ## Attempt to install system dependencies
	asdf plugin add python || asdf plugin update python
	asdf plugin add pdm || asdf plugin update pdm
	asdf install

.PHONY: doctor
doctor: ## Confirm system dependencies are available
	bin/verchew

# PROJECT DEPENDENCIES ########################################################

DEPENDENCIES := target/.pdm-$(shell bin/checksum pyproject.toml pdm.lock)

.PHONY: install
install: $(DEPENDENCIES) .cache ## Install project dependencies

$(DEPENDENCIES): pdm.lock
	@ rm -rf target/.pdm-*
	pdm install
	pdm run pre-commit install
	@ touch $@

pdm.lock: pyproject.toml
	pdm lock
	@ touch $@

.cache:
	@ mkdir -p .cache

# CHECKS ######################################################################

.PHONY: check
check: install  ## Run formaters, linters, and static analysis
	pdm lock --check
	pdm run pre-commit run -a
	pdm run mypy
	pdm run deptry .

# TESTS #######################################################################

.PHONY: test
test: install  ## Run unit and integration tests
	pdm run pytest --random --doctest-modules

.PHONY: test-repeat
test-repeat: install
	pdm run pytest --count=5 --random --doctest-modules --exitfirst

# RELEASE #####################################################################

DIST_FILES := dist/*.tar.gz dist/*.whl

.PHONY: dist
dist: install $(DIST_FILES)
$(DIST_FILES): $(MODULES) pyproject.toml
	rm -f $(DIST_FILES)
	pdm build

.PHONY: upload
upload: dist  ## Upload the current version to PyPI
	git diff --name-only --exit-code
	pdm publish
	bin/open https://pypi.org/project/$(PACKAGE)

# CLEANUP #####################################################################

.PHONY: clean
clean:  ## Delete all generated and temporary files
	rm -rf .venv
	rm -rf dist
	rm -rf target
	rm -rf src/rust/target

# HELP ########################################################################

.PHONY: help
help: install
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
