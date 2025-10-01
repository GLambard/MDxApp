# Makefile for MDxApp Development
# Provides convenient commands for common tasks

.PHONY: help install install-dev format lint type-check test test-cov clean all pre-commit

# Default target
help:
	@echo "MDxApp Development Commands"
	@echo "============================"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install production dependencies"
	@echo "  make install-dev    - Install development dependencies"
	@echo "  make pre-commit     - Setup pre-commit hooks"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format         - Format code with Black"
	@echo "  make lint           - Lint code with Ruff"
	@echo "  make type-check     - Type check with Mypy"
	@echo "  make security       - Security scan with Bandit"
	@echo "  make all            - Run all quality checks"
	@echo ""
	@echo "Testing:"
	@echo "  make test           - Run tests with pytest"
	@echo "  make test-cov       - Run tests with coverage report"
	@echo "  make test-html      - Run tests and open HTML coverage report"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove cache files and build artifacts"
	@echo ""

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

# Setup pre-commit hooks
pre-commit:
	pre-commit install
	@echo "Pre-commit hooks installed!"

# Code formatting
format:
	@echo "Running Black formatter..."
	black src/ tests/
	@echo "Formatting complete!"

# Linting
lint:
	@echo "Running Ruff linter..."
	ruff check src/ tests/ --fix
	@echo "Linting complete!"

# Type checking
type-check:
	@echo "Running Mypy type checker..."
	mypy src/
	@echo "Type checking complete!"

# Security scanning
security:
	@echo "Running Bandit security scanner..."
	bandit -c pyproject.toml -r src/
	@echo "Security scan complete!"

# Run all quality checks
all: format lint type-check security
	@echo ""
	@echo "All quality checks complete!"

# Testing
test:
	@echo "Running tests..."
	pytest

test-cov:
	@echo "Running tests with coverage..."
	pytest --cov=src --cov-report=term-missing --cov-report=html

test-html: test-cov
	@echo "Opening coverage report..."
	@if command -v open > /dev/null; then \
		open htmlcov/index.html; \
	elif command -v xdg-open > /dev/null; then \
		xdg-open htmlcov/index.html; \
	else \
		echo "Coverage report generated in htmlcov/index.html"; \
	fi

# Cleanup
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	rm -rf htmlcov/ dist/ build/ .eggs/ 2>/dev/null || true
	@echo "Cleanup complete!"

# Run Streamlit app (convenience)
run:
	streamlit run MDxApp/01_🏥_Diagnosis_Assistant.py

# Show file counts and stats
stats:
	@echo "Project Statistics"
	@echo "=================="
	@echo ""
	@echo "Python files:"
	@find src/ tests/ -name "*.py" | wc -l
	@echo "Lines of code (src/):"
	@find src/ -name "*.py" -exec cat {} \; | wc -l
	@echo "Lines of tests:"
	@find tests/ -name "*.py" -exec cat {} \; | wc -l
	@echo ""

