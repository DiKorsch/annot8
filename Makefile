
UID := $(shell id -u)
GID := $(shell id -g)

export UID
export GID

build: build_ui build_docker

install:
	@echo "INSTALL MISSING!"

run_backend:
	@cd backend && python manage.py runserver

run_frontend:
	@cd frontend && npm run serve

run_docker: build_docker
	@echo "DOCKER START MISSING!"

backend_tests:
	backend/manage.py test

backend_coverage:
	coverage run backend/manage.py test
	coverage html
	coverage report -m

backend_pylint:
	@echo "BACKEND PYLINT MISSING!"


build_ui:
	npm run build

build_docker:
	docker build . \
		--tag annot8:latest \
		--build-arg UID=${UID} \
		--build-arg GID=${GID}

