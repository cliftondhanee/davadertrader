fmt:
	isort .
	flynt --quiet .
	black .

lint:
	flake8 .
	flynt --dry-run --fail-on-change --quiet .
	isort --diff --check .
	black --diff --check .
	mypy .
	yamllint .

requirements:
	pip install pip-tools
	pip-compile
	pip install -r requirements.txt

coverage:
	coverage xml
	coverage report || true

run:
	python run.py

