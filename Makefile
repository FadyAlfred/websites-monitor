DOCKER ?= docker

local-isntall:
	pipenv install -d

local-run-migration:
	PYTHONPATH=. python aiven_monitor/main.py --loglevel INFO run-migration

local-run-website-seeding:
	PYTHONPATH=. python aiven_monitor/main.py --loglevel INFO run-database-website-seeding

local-run-monitor-consumer:
	PYTHONPATH=. python aiven_monitor/main.py --loglevel INFO run-monitor-event-consumer

local-run-monitor-producer:
	PYTHONPATH=. python  aiven_monitor/main.py --loglevel INFO run-monitor-event-producer

local-run-unit-tests:
	PYTHONPATH=. coverage run -m pytest tests

local-show-coverage:
	PYTHONPATH=. coverage report

local-run-code-checks:
	PYTHONPATH=. pytype . && flake8


docker-install:
	docker build . -t aiven_monitor:1.0

docker-run-migration:
	docker run --env-file .env aiven_monitor:1.0 --loglevel INFO run-migration

docker-run-db-website-seeding:
	docker run --env-file .env aiven_monitor:1.0 --loglevel INFO run-database-website-seeding

docker-run-monitor-consumer:
	docker run --env-file .env aiven_monitor:1.0 --loglevel INFO run-monitor-event-consumer

docker--run-monitor-producer:
	docker run --env-file .env aiven_monitor:1.0 --loglevel INFO run-monitor-event-producer

