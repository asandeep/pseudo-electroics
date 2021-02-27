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
