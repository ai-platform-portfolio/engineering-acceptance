STANDARDS ?= ../engineering-standards
PYTHON ?= python3
.PHONY: test
test:
	$(PYTHON) scripts/run_acceptance.py --checker $(abspath $(STANDARDS))/.venv/bin/engineering-checks --tools $(abspath $(STANDARDS))/node_modules/.bin
