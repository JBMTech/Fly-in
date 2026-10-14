MAP ?= map

install:
		uv sync --all-groups

run:
		uv run python -m src.main $(MAP)

help:
	@echo "=================================================="
	@echo "make install        install dependencies"
	@echo "make run            run the simulation"
	@echo "make debug          run under pdb"
	@echo "make clean          remove caches"
	@echo "make fclean         remove caches and simulation"
	@echo "make lint           run flake8 + mypy"
	@echo "=================================================="

debug:
		uv run python -m pdb -m src.main $(MAP)

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