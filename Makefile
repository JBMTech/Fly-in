MAP ?= map

# Colores y estilos
RED    := \033[0;31m
GREEN  := \033[0;32m
YELLOW := \033[0;33m
BLUE   := \033[0;34m
CYAN   := \033[0;36m
RESET  := \033[0m

install:
	@echo "$(CYAN)📦 Instalando dependencias del proyecto con uv...$(RESET)"
	uv sync --all-groups
	@echo "$(GREEN)✅ ¡Entorno instalado correctamente!$(RESET)"

run:
	@echo "$(BLUE)🚀 Iniciando la simulación con el mapa: '$(MAP)'...$(RESET)"
	uv run python -m src.main $(MAP)

help:
	@echo "$(CYAN)==================================================$(RESET)"
	@echo "🔍 $(BLUE)Comandos disponibles en este proyecto:$(RESET)"
	@echo "$(CYAN)==================================================$(RESET)"
	@echo "  $(GREEN)make install$(RESET)        Instalar dependencias del proyecto"
	@echo "  $(GREEN)make run$(RESET)            Ejecutar la simulación ($(YELLOW)MAP=nombre$(RESET) opcional)"
	@echo "  $(GREEN)make debug$(RESET)          Ejecutar bajo el depurador (pdb)"
	@echo "  $(GREEN)make lint$(RESET)           Ejecutar análisis estático (flake8 + mypy)"
	@echo "  $(GREEN)make lint-strict$(RESET)    Ejecutar análisis estático estricto"
	@echo "  $(GREEN)make clean$(RESET)          Eliminar archivos de caché"
	@echo "  $(GREEN)make fclean$(RESET)         Eliminar cachés y el entorno virtual (.venv)"
	@echo "  $(GREEN)make help$(RESET)           Ver este menú de ayuda"
	@echo "$(CYAN)==================================================$(RESET)"

debug:
	@echo "$(YELLOW)🐞 Iniciando modo depuración (pdb) con mapa: '$(MAP)'...$(RESET)"
	uv run python -m pdb -m src.main $(MAP)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@echo "$(GREEN)🧹 Cachés eliminadas correctamente ✓$(RESET)"

fclean: clean
	@rm -rf .venv
	@echo "$(GREEN)🗑️  Entorno virtual (.venv) eliminado ✓$(RESET)"

lint:
	@echo "$(CYAN)✨ Ejecutando linters (flake8 + mypy)...$(RESET)"
	@uv run flake8 --exclude=.venv && \
	 uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude '^(venv|\.venv|env)/' && \
	 echo "$(GREEN)✅ ¡Código limpio! Todo en orden. $(RESET)" || \
	 (echo "$(RED)❌ Se encontraron errores en el código. Revisa los mensajes de arriba.$(RESET)" && exit 1)

lint-strict:
	@echo "$(YELLOW)🛡️  Ejecutando linters en modo ESTRICTO...$(RESET)"
	@uv run flake8 --exclude=.venv && \
	 uv run mypy . \
		--strict \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--exclude '^(venv|\.venv|env)/' && \
	 echo "$(GREEN)🌟 ¡Excelente! Código impecable bajo reglas estrictas.$(RESET)" || \
	 (echo "$(RED)❌ El código no cumple con el estándar estricto.$(RESET)" && exit 1)

.PHONY: install run help debug clean fclean lint lint-strict
