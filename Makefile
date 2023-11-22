# --------- Development commands ---------

format: # Format code and sort imports
	poetry run black swap_user
	poetry run isort swap_user

lint: # Run code quality tools
	# Check pep8 style
	poetry run flake8 swap_user
	# Check imports order
	poetry run isort swap_user --check-only
	# Check security issues with installed packages
	poetry run safety check

# Prevent running a file with same name
.PHONY: test
test: # Run tests
	poetry run tox


# --------- GitHub Actions CI ---------

# Prevent running a file with same name
.PHONY: test

ci.lint: # Run code quality tools inside ci
	# Check pep8 style
	poetry run flake8 swap_user
	# Check imports order
	poetry run isort swap_user --check-only
	# Check security issues with installed packages
	poetry run safety check