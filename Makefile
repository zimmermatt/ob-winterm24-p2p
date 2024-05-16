.PHONY: clean clean-build clean-src pylint ruff run test

.DEFAULT_GOAL := test

clean: clean-build clean-src

clean-build:
	@echo ">>> Cleaning build"
	rm -rf build

clean-src:
	@echo ">>> Cleaning source"
	find src/ -type d -name "__pycache__" -print0 | xargs -0 rm -rf

pylint:
	pylint --recursive=y src/*/py

ruff-check:
	ruff format --check .
	ruff check .

ruff-format:
	ruff format .

run:
	export PYTHONPATH=src/main/py; \
		python -m peer.peer 50000 "src/test/py/resources/peer_test" "0.0.0.0:50000"

<<<<<<< frontend
frontend:
	export PYTHONPATH=src/main/py; \
	./devops/deploy/spin-up-script.sh &
	export PYTHONPATH=src/main/py; \
	python src/main/py/frontend/frontend.py 50050 "keys/node50" "127.0.0.1:50000"

test: ruff pylint
=======
test: ruff-check pylint
>>>>>>> main
	export PYTHONPATH=src/main/py; \
	    coverage run -m unittest discover --pattern "*_test.py" \
		  --start-directory src/test/py \
		  --top-level-directory .
	coverage report
	coverage html

container:
	podman build -t myapp .
	podman run --rm -i myapp < input.txt

container-test: ruff pylint
	podman build -t myapp .
	podman run --rm -i myapp < input.txt sh -c '\
	coverage run -m unittest discover --pattern "*_test.py" --start-directory src/test/py --top-level-directory .; \
	coverage report; \
	coverage html'
