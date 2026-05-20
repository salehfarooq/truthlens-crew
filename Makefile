.PHONY: install test lint demo dashboard

install:
	python -m pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src tests

demo:
	truthlens verify "Pakistan gained independence in 1947."
	truthlens benchmark data/sample/claims.csv

dashboard:
	truthlens dashboard

