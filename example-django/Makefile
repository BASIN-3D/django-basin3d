.PHONY: all

PYTHON=python3.8

all: bin-python db.sqlite3

docs:
	cd $(CURDIR)/../docs; PYTHONPATH=$(CURDIR) DJANGO_SETTINGS_MODULE=mybroker.settings make html

develop:
	$(CURDIR)/bin/pip install -e ".[dev]"

bin-python:
	$(PYTHON) -m venv .
	$(CURDIR)/bin/pip install -e ".[dev]"

db.sqlite3:
	$(CURDIR)/bin/python manage.py migrate


.PHONY: run
run:
	PYTHONPATH=$(PYTHONPATH):$(CURDIR)/..:. bin/python manage.py runserver

.PHONY: clean
clean:
	rm -rf bin lib  include build var db.sqlite3
	find  ./ -name *.pyc -exec rm {} +
