
install:
	python3 -m venv .
	bin/pip install bottle elasticsearch

run:
	bin/python server.py
