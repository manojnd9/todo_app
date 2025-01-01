# Format
make format:
	poetry run black .

# Format Check
make format_check:
	poetry run black --check .

# Testing
make test:
	poetry run pytest . --cov=todo_app