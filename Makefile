.PHONY: pylint ruff run test

.DEFAULT_GOAL := test

pylint:
	pylint --recursive=y src/*/py

ruff:
	ruff format
	ruff .

run:
	export PYTHONPATH=src/main/py; \
		python3 -m sample_module.udp_server 42422

test: ruff pylint
	export PYTHONPATH=src/main/py; \
	python3 -m unittest discover --pattern "*_test.py" --start-directory src/test/py --top-level-directory .

clean-env:
	@echo "I'm cleaning the environment OwO"
	command -v deactivate && deactivate
	rm -rf venv

clean-src:
	@echo "Cleaning source"
	find src/ -type d -name "__pycache__" -print0 | xargs -0 rm -rf
