.PHONY: default icons verify venv clean

default: icons

icons:
	@test -d .venv || $(MAKE) venv
	.venv/bin/python build/generate_icons.py

# Compare the current mono/ + color/ icons against the last commit
# (run after `make icons` to check for unexpected changes).
verify:
	@test -d .venv || $(MAKE) venv
	@dir=$$(mktemp -d); \
	trap 'rm -rf "$$dir"' EXIT; \
	git archive HEAD mono/icons color/icons | tar -x -C "$$dir"; \
	.venv/bin/python build/compare_icons.py "$$dir" .

venv:
	python3 -m venv .venv
	.venv/bin/pip install --quiet -r requirements.txt

clean:
	rm -rf .venv
