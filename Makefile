all:
	./setup.py build

install: venv
	./.venv/Scripts/python -m pip install -r ./requirements.txt

install-dev: venv
	./.venv/Scripts/python -m pip install -r ./dev-requirements.txt

venv:
	python -m venv .venv

clean:
	rm -rf ./.venv

.PHONY: all install install-dev venv clean