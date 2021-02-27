DOCKER_IMAGE_NAME := pseudo-electronics
DOCKER_IMAGE_TAG := latest

CURRENT_APP_VERSION := $(lastword $(shell poetry version))

setup:
	python manage.py migrate
	python manage.py loaddata fixtures.yaml --format yaml
	python manage.py sync_roles --reset_user_permissions
	python manage.py createsuperuser


clear-db:
	rm db.sqlite3


reset: clear-db setup


server:
	SHOW_DEBUG_TOOLBAR=false python manage.py runserver


docker:
	# Export project dependencies to requriements file. Include dev dependencies
	# for now.
	poetry export -f requirements.txt -o requirements.txt --dev --without-hashes

	docker build \
		-t ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} \
		-t $(DOCKER_IMAGE_NAME):$(CURRENT_APP_VERSION) .

	rm requirements.txt
