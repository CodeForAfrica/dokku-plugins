ROOT_DIR := $(shell dirname "$(realpath $(firstword $(MAKEFILE_LIST)))")

all: build

## display this message
help:
	@echo  ''
	@echo  'Usage:'
	@echo  'make <target>'
	@echo  ''
	@echo  'Targets:'
	@awk '/^##/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t
	@echo  ''

## tidy up local dev environment
clean:
	rm -rf __pycache__ .mypy_cache build

## build all plugins
build: build-pr-db-mongo

## build 'pr-db-mongo' plugin
build-pr-db-mongo: make-build-dir
	rm -rf pr-db-mongo/venv
	tar --create --no-xattrs --disable-copyfile --file build/pr-db-mongo.tgz pr-db-mongo

# create 'build' output dir
make-build-dir:
	mkdir -p build

## check and format code
lint:
	pre-commit run --all-files

.PHONY: all build build-pr-db-mongo clean help lint make-build-dir
