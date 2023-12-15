
UID := $(shell id -u)
GID := $(shell id -g)

export UID
export GID

DOCKER_OPTS :=

docker.run.dev:
	docker compose --env-file .env.local --profile dev up $(DOCKER_OPTS)

docker.build.dev:
	docker compose --env-file .env.local --profile dev build $(DOCKER_OPTS)

docker.run:
	docker compose --env-file .env --profile production up $(DOCKER_OPTS)

docker.build:
	docker compose --env-file .env --profile production build $(DOCKER_OPTS)


install:
	@echo "INSTALL MISSING!"

run_backend:
	@cd backend && python manage.py runserver

run_frontend:
	@cd frontend && npm run serve

backend_tests:
	@cd backend && python manage.py test

backend_coverage:
	@cd backend && coverage run manage.py test
	coverage html
	coverage report -m

backend_pylint:
	@echo "BACKEND PYLINT MISSING!"

start_screen:
	screen -dmS annot8 -c scripts/screen/rc

