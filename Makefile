.DEFAULT_GOAL := help
.PHONY: clean pep8 black lint test install

PYLINT          := pylint
PYTEST          := pytest
PEP8            := flake8
BLACK           := black
MYPY            := mypy
PIP             := pip

clean:
	rm -fr build
	rm -fr dist
	rm -fr *.egg-info
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;
	rm -rf $$(find . -name '__pycache__')
	rm -rf $$(find . -name '.mypy_cache')
	rm -rf .pytest_cache

pep8:
	$(PEP8) pymdot tests

black:
	$(BLACK) .

lint:
	$(PYLINT) pymdot # --rcfile=setup.cfg

mypy:
	$(MYPY) --ignore-missing-imports -p pymdot

test:
	$(PYTEST) -v

install:
	$(PIP)  install -r requirements.txt

help:
	@echo "Available targets:"
	@echo "- clean       Clean up the source directory"
	@echo "- pep8        Check style with flake8"
	@echo "- lint        Check style with pylint"
	@echo "- black       Check style with black"
	@echo "- mypy        Check type hinting with mypy"
	@echo "- test        Run tests using pytest"
	@echo
	@echo "Available variables:"
	@echo "- PYLINT      default: $(PYLINT)"
	@echo "- PYTEST      default: $(PYTEST)"
	@echo "- PEP8        default: $(PEP8)"
	@echo "- BLACK       default: $(BLACK)"
	@echo "- MYPY        default: $(MYPY)"
	@echo "- PIP         default: $(PIP)"
