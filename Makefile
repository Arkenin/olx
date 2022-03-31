build:
	docker-compose build

up:
	docker-compose up -d app

test:
	pytest -v -s

logs:
	docker-compose logs app | tail -50

down:
	docker-compose down

all: down build up
