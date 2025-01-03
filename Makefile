# Format
make format:
	poetry run black .

# Format Check
make format_check:
	poetry run black --check .

# Testing
make test:
	poetry run pytest . --cov=todo_app

# Export requirements.txt
make requirements:
	poetry export --without-hashes --format=requirements.txt --output requirements.txt