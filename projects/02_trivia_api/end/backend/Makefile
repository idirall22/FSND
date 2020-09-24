POSTGRES_CONTAINER_NAME=api-postgres

print:
	@echo "run 'make postgres-up' to start postgres container."
	@echo "run 'make postgres-down' to delete postgres container."
	@echo "run 'make connect' to connect with postgres database container."
	@echo "run 'make populate' to populate trivia database with dump data."
	@echo "run 'make env' to create virtualenv"
	@echo "run 'make freeze' to create requirements.txt"
	@echo "run 'make install' to install requirements.txt"
	@echo "run 'make run' to start server"

install:
	pip3 install -r requirements.txt

# migrate: clear-migration
# 	flask db init
# 	flask db migrate -m "Initial migration."
# 	flask db upgrade	

# clear-migration:
# 	rm -rf migrations

connect:
	docker exec -it $(POSTGRES_CONTAINER_NAME) sh -c "psql -U postgres"

postgres-up:
	docker run \
	--name $(POSTGRES_CONTAINER_NAME) \
	-e POSTGRES_PASSWORD=password \
	-e POSTGRES_USER=postgres \
	-e POSTGRES_DB=trivia \
	-p 5432:5432 \
	-d postgres

postgres-down:
	docker rm -f $(POSTGRES_CONTAINER_NAME)

populate:
	docker cp trivia.psql $(POSTGRES_CONTAINER_NAME):/trivia.psql
	docker exec $(POSTGRES_CONTAINER_NAME) sh -c "psql -U postgres -d trivia -c '\i trivia.psql'"
	
run:
	export FLASK_APP=myapp
	export FLASK_ENV=development
	python3 app.py

env:
	virtualenv env

freeze:
	 pip3 freeze > requirements.txt