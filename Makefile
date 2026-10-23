.PHONY: default icons venv clean

default: icons

icons:
	@test -d .venv || $(MAKE) venv
	.venv/bin/python build/generate_icons.py

venv:
	python3 -m venv .venv
	.venv/bin/pip install --quiet -r requirements.txt

clean:
	rm -rf .venv
