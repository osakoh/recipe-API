build:
	docker compose build

flake8:
	docker compose run --rm app sh -c flake8

up:
	docker compose up

down:
	docker compose down


#delete:
#	#docker compose kill $(docker ps -q)
#	docker rm $(call args, docker ps -a -q)
#	docker rmi $(docker images -q)
#	docker system prune -f
#	docker volume prune -f