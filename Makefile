build:
	docker compose build

flake8:
	docker compose run --rm app sh -c "flake8"

up:
	docker compose up

down:
	docker compose down

logs:
	docker compose logs


migrate:
	docker compose run --rm app sh -c "python3 manage.py migrate"


migrations:
	docker compose  run --rm app sh -c "python3 manage.py makemigrations"

db:
	docker compose  run --rm app sh -c "python3 manage.py wait_for_db && flake8"


flush:
	docker compose  run --rm app sh -c "python3 manage.py flush"


collectstatic:
		docker compose  run --rm app sh -c "python3 manage.py collectstatic --noinput --clear"


superuser:
		docker compose  run --rm app sh -c "python3 manage.py createsuperuser"


bash:
	docker compose exec -it app sh


test:
	docker compose run --rm app sh -c "python3 manage.py test"

activate:
	source .venv/Scripts/activate


other:
	docker compose run --rm app sh -c "python manage.py test core.tests.test_health_check.HealthCheckTests.test_health_check"

