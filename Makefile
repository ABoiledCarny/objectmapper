NPROC := $(shell nproc)
PKG_NAME := objectmapper

sure: typecheck lint testall coverage

test:
	pytest

testall:
	tox -c tox.ini -p $(NPROC)

lint:
	pylint --rcfile .pylintrc $(PKG_NAME)

typecheck:
	pytype --config .pytyperc $(PKG_NAME)

coverage:
	pytest --cov-config .coveragerc --cov=$(PKG_NAME)

.PHONY: docs
docs: doctest
	cd docs && make clean && make html

doctest:
	cd docs && make doctest

publish: sure docs
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg $(PKG_NAME).egg-info

clean:
	rm -fr build dist .egg $(PKG_NAME).egg-info
