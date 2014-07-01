SHELL := /bin/bash

help:
	@echo "usage:"
	@echo "    make release -- build and release to PyPI"

release:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload dist/*
