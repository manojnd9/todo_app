# Format
make format:
	poetry run black .

# Format Check
make format_check:
	poetry run black --check .