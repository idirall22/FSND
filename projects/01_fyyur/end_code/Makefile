POSTGRES_CONTAINER_NAME=fyyur-postgres

install:
	pip3 install -r requirements.txt

migrate: clear-migration
	flask db init
	flask db migrate -m "Initial migration."
	flask db upgrade	

clear-migration:
	rm -rf migrations

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
	export FLASK_APP=myapp
	export FLASK_ENV=development
	python3 app.py

env:
	virtualenv env

freeze:
	 pip3 freeze > requirements.txt