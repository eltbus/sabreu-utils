check:
	@uv run python -Bm ruff check sabreu_utils tests

format:
	@uv run python -Bm ruff format sabreu_utils tests
