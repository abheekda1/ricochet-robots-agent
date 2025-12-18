.PHONY: build singletest test

RUNS ?= 5

build:
	echo '#!/bin/bash' > test
	echo 'exec pypy3 test.py "$$@"' >> test
	chmod u+x test

test:
	./test $(RUNS)

singletest:
	./test