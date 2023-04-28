.PHONY: tests_all test-file book serve

tests_all:
	poetry run pytest -v -rP

test-file:
	poetry run pytest -v -rP $(file)

postgres:
	cd remindme/db/postgres \
	&& docker-compose up

postgres-delete:
	cd remindme/db/postgres && docker-compose down --volumes --remove-orphans