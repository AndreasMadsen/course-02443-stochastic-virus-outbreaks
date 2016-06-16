
.PHONY: all test lint

all: test lint

test:
	nosetests code/tests/*

lint:
	pep8 code
