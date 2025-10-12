SHELL := /bin/bash
PWD := $(shell pwd)

all:

build-system:
	docker build -f ./Dockerfile -t "player-api:latest" .
.PHONY: build-system

up: build-system
	docker compose -f docker-compose.yaml up -d --build --remove-orphans
.PHONY: up

down:
	docker compose -f docker-compose.yaml down
.PHONY: down

test:
	python -m pytest --cov=src --cov-report=xml tests/test_main.py -v
.PHONY: test