
test:
	ruff format
	ruff .
	pylint --recursive=y src/*/py
	export PYTHONPATH=src/main/py; \
	python3 -m unittest discover --pattern "*_test.py" --start-directory src/test/py --top-level-directory .

run:
	export PYTHONPATH=src/main/py; \
		python3 -m sample_module.udp_server 42422

