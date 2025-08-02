.PHONY: help setup install dev-install test lint format type-check clean collect-doc collect-docs

# Default target
help:
	@echo "Available targets:"
	@echo "  setup           - Set up development environment"
	@echo "  install         - Install package"
	@echo "  dev-install     - Install package in development mode"
	@echo "  test            - Run tests"
	@echo "  lint            - Run linting"
	@echo "  format          - Format code"
	@echo "  type-check      - Run type checking"
	@echo "  clean           - Clean build artifacts"
	@echo "  collect-doc     - Collect single document (usage: make collect-doc FILE=path_or_url)"
	@echo "  collect-docs    - Collect multiple documents (usage: make collect-docs FILES='file1 file2 ...')"

# Development environment setup
setup:
	@echo "Setting up development environment..."
	python -m pip install --upgrade pip
	pip install uv
	uv sync --dev

# Install package
install:
	uv pip install .

# Install in development mode
dev-install:
	uv pip install -e .

# Run tests
test:
	pytest

# Run linting
lint:
	ruff check src tests

# Format code
format:
	ruff format src tests

# Run type checking
type-check:
	mypy src

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Document collection targets
collect-doc:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make collect-doc FILE=<path_or_url>"; \
		echo "Example: make collect-doc FILE=/path/to/document.pdf"; \
		echo "Example: make collect-doc FILE=https://example.com/doc.pdf"; \
		exit 1; \
	fi
	@echo "Collecting document: $(FILE)"
	collect-doc "$(FILE)"

collect-docs:
	@if [ -z "$(FILES)" ]; then \
		echo "Usage: make collect-docs FILES='file1 file2 ...'"; \
		echo "Example: make collect-docs FILES='/path/doc1.pdf /path/doc2.docx'"; \
		exit 1; \
	fi
	@echo "Collecting documents: $(FILES)"
	@for file in $(FILES); do \
		echo "Processing: $$file"; \
		collect-doc "$$file"; \
	done

# Development workflow
dev: dev-install lint type-check test

# CI workflow
ci: install lint type-check test
