MAP ?= map

# Colors and styles
RED    := \033[0;31m
GREEN  := \033[0;32m
YELLOW := \033[0;33m
BLUE   := \033[0;34m
CYAN   := \033[0;36m
RESET  := \033[0m

install:
	@echo "$(CYAN)📦 Installing project dependencies with uv...$(RESET)"
	uv sync --all-groups
	@echo "$(GREEN)✅ Environment installed successfully!$(RESET)"

run:
	@echo "$(BLUE)🚀 Starting simulation with map: '$(MAP)'...$(RESET)"
	uv run python -m src.main $(MAP)

help:
	@echo "$(CYAN)==================================================$(RESET)"
	@echo "🔍 $(BLUE)Available project commands:$(RESET)"
	@echo "$(CYAN)==================================================$(RESET)"
	@echo "  $(GREEN)make install$(RESET)        Install project dependencies"
	@echo "  $(GREEN)make run$(RESET)            Run the simulation ($(YELLOW)MAP=name$(RESET) optional)"
	@echo "  $(GREEN)make debug$(RESET)          Run under the Python debugger (pdb)"
	@echo "  $(GREEN)make lint$(RESET)           Run static analysis (flake8 + mypy)"
	@echo "  $(GREEN)make lint-strict$(RESET)    Run strict static analysis"
	@echo "  $(GREEN)make clean$(RESET)          Remove cache files"
	@echo "  $(GREEN)make fclean$(RESET)         Remove caches and the virtual environment (.venv)"
	@echo "  $(GREEN)make help$(RESET)           Display this help menu"
	@echo "$(CYAN)==================================================$(RESET)"

debug:
	@echo "$(YELLOW)🐞 Starting debug mode (pdb) with map: '$(MAP)'...$(RESET)"
	uv run python -m pdb -m src.main $(MAP)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@echo "$(GREEN)🧹 Caches removed successfully! ✓$(RESET)"

fclean: clean
	@rm -rf .venv
	@echo "$(GREEN)🗑️  Virtual environment (.venv) removed! ✓$(RESET)"

lint:
	@echo "$(CYAN)✨ Running linters (flake8 + mypy)...$(RESET)"
	@uv run flake8 --exclude=.venv && \
	 uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude '^(venv|\.venv|env)/' && \
	 echo "$(GREEN)✅ Code quality checks passed! Everything looks good. $(RESET)" || \
	 (echo "$(RED)❌ Code quality issues found. Check the messages above.$(RESET)" && exit 1)

lint-strict:
	@echo "$(YELLOW)🛡️  Running linters in STRICT mode...$(RESET)"
	@uv run flake8 --exclude=.venv && \
	 uv run mypy . \
		--strict \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude '^(venv|\.venv|env)/' && \
	 echo "$(GREEN)🌟 Excellent! Code meets the strict quality standards. $(RESET)" || \
	 (echo "$(RED)❌ Code does not meet the strict quality standards.$(RESET)" && exit 1)

.PHONY: install run help debug clean fclean lint lint-strict
