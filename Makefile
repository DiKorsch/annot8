
UID := $(shell id -u)
GID := $(shell id -g)

export UID
export GID

run_backend:
	@cd backend && python manage.py runserver

run_frontend:
	@cd frontend && npm run serve

install:
	@echo "INSTALL MISSING!"


backend_tests:
	@echo "BACKEND TESTS MISSING!"

backend_coverage:
	@echo "BACKEND COVERAGE MISSING!"

backend_pylint:
	@echo "BACKEND PYLINT MISSING!"


docker_build:
	docker build . \
		--tag annot8:latest \
		--build-arg UID=${UID} \
		--build-arg GID=${GID}

docker_start: docker_build
	@echo "DOCKER START MISSING!"

