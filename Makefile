init:
	python3 -m venv venv

install:
	pip install -r requirements.txt

build-package:
	python ./setup.py install

format:
	yapf -r -i --style google integraty/*.py

install-venv:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	source venv/bin/activate && python ./setup.py install

documentation: integraty/case.py integraty/extprog.py integraty/productivity.py integraty/xstring.py
	handsdown -n integraty \
	--exclude integraty/sandbox.py \
	--external https://github.com/szaydel/integraty/blob/master/ \
	integraty

test:
	pytest -v tests

.PHONY: all

all: build-package test
