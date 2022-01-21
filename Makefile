install:
	poetry install

page-loader:
	poetry run page_loader -h

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

make lint:
	poetry run flake8 page_loader
	
run_test:
	poetry run pytest --cov=page_loader tests/ --cov-report xml