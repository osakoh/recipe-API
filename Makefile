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

