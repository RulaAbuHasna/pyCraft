# run linting
lint:
	ruff check .

# run tests
test:
	PYTHONPATH=. pytest utils/tests

# build package
build:
	python setup.py sdist bdist_wheel

# publish package
publish:
	python -m twine upload dist/*

# clean up
clean:
	rm -rf dist build


