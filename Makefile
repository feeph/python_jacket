# a super-trivial makefile

.PHONY: test

test:
	PYTHONPATH=jacket python3 -m pytest tests/
