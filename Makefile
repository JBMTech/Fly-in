MAP ?= map

install:
		uv sync --all-groups

run:
		uv run python -m src.main $(MAP)

debug:
		uv run python3 -m pdb -m src $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

fclean: clean
	rm -rf .venv

lint:
	uv run flake8 --exclude=.venv
	uv run mypy . \
			--warn-return-any \
	        --warn-unused-ignores \
            --ignore-missing-imports \
            --disallow-untyped-defs \
            --check-untyped-defs \
            --exclude '^(venv|\.venv|env)/'

.PHONY: install run debug clean fclean lint