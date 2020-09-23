POSTGRES_CONTAINER_NAME=fyyur-postgres

migrate:
	flask db init
	flask db migrate -m "Initial migration."
	flask db upgrade

clear-migration:
	rm -r migrations

connect:
	docker exec -it $(POSTGRES_CONTAINER_NAME) sh

postgres-up:
	docker run \
	--name $(POSTGRES_CONTAINER_NAME) \
	-e POSTGRES_PASSWORD=password \
	-e POSTGRES_USER=postgres \
	-e POSTGRES_DB=fyyur \
	-p 5432:5432 \
	-d postgres

postgres-down:
	docker rm -f $(POSTGRES_CONTAINER_NAME)

run:
	python3 app.py

