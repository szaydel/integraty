init:
	python3 -m venv venv
install:
	python ./setup.py install
format:
	yapf -r -i --style google integraty/*.py

documentation: integraty/case.py integraty/extprog.py integraty/productivity.py integraty/xstring.py
	handsdown -n integraty \
	--exclude integraty/sandbox.py \
	--external https://github.com/szaydel/integraty/blob/master/ \
	integraty