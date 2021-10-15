run-dev:
	poetry run sanic user_api.main:app --auto-reload --host 0.0.0.0 --port 5000

format:
	@poetry run black .
	@poetry run isort .
	@poetry run autoflake --remove-all-unused-imports --remove-unused-variables --remove-duplicate-keys --expand-star-imports -ir .