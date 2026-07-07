.PHONY: install test demo clean

# Install in editable mode
install:
	pip install -e ".[dev]"

# Run tests
test:
	pytest tests/ -v --tb=short

# Run demo
demo:
	python -m agent_spark.filter.five_layer_filter --help
	agent-spark-demo

# Run filter engine on a JSON file
filter:
	python -m agent_spark.filter.five_layer_filter $(FILE)

# Clean generated files
clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ __pycache__/
	find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete

# Build distribution packages
dist:
	python -m pip install --upgrade build
	python -m build

# Upload to PyPI (requires credentials)
upload:
	python -m twine upload dist/*

# List project files
tree:
	find . -not -path './.git/*' -not -path './__pycache__/*' -not -path './*.egg-info/*' -not -name '*.pyc' -not -name '.DS_Store' | sort

