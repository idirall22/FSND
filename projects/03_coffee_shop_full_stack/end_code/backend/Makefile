POSTGRES_CONTAINER_NAME=api-postgres
include .env

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
	pip3 install -r requirements.txt --ignore-installed

migrate: clear-migration
	flask db init
	flask db migrate -m "Initial migration."
	flask db upgrade	

clear-migration:
	rm -rf migrations

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
	flask run --reload

env:
	virtualenv env

freeze:
	 pip3 freeze > requirements.txt
	 
test:
	python -m unittest discover -p 'test_*.py'

.PHONY: 
	run freeze env populate postgres-up postgres-down install test

# curl -X POST -H 'Content-Type: application/json' -d '{"title": "espresso2", "recipe": [{"color": "white", "name": "milk", "parts":1}]}'  http://localhost:5000/drinks
# curl -X POST -H "Authorization: bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imp6RjJhNlloWmVlREc5WTh3MWJuciJ9.eyJpc3MiOiJodHRwczovL2Rldi1tNzloNnN5NC5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZhNmVjYjhjYWUwMzIwMDcxOWZiNzIyIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNjA0Nzc1NzgzLCJleHAiOjE2MDQ3ODI5ODMsImF6cCI6Iks5TGZ4QXJTQmZEclVuT1NVR1h3WkFSbGJOQzU1Vm8zIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.nG1bikxyMtGPaZJhJaZiTTGDS8fw2msJrDuHfbFIpcO6A7G_RkLTHg0B9Wzi5ODaDyy9_GNvn611CEja0w_ht0cDKFqd449fXBTQODAoXyyPfSTPHs8oZ1Lg7_aKMaWdfIUIMFE5Ni_Owd8jPcwAQmPCVKTuUTuD5l4je73nOgF8CqMfpvaUPng0zbLzIvffLTNCLGwMc99B1YustEg1taJVvAj3De-pgGNNk6GDRqdNKn67A7a971DdkXPCcIQKGquYYA4Lhm1152i3oXB9uOOyVX9m8W68m1QqAjUb3hWG5psV1MpflI9vA_secM4cDEhnMcwUMTWyt8DVmunpZA" \
# -H 'Content-Type: application/json' -d '{"title": "espresso2", "recipe": [{"color": "white", "name": "milk", "parts":1}]}'  http://localhost:5000/drinks
# curl -X PATCH -H 'Content-Type: application/json' -d '{"title": "Expresso", "recipe": [{"color": "brown", "name": "cannel", "parts":1}, {"color": "white", "name": "milko", "parts":2}]}'  http://localhost:5000/drinks/1
# curl http://localhost:5000/drinks
# curl http://localhost:5000/drinks-detail