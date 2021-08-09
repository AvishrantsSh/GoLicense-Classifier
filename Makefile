PYTHON_EXE?=python3

package: format test
	@echo "-> Clearing Redundant Build Files"
	@rm -rf dist || true
	@rm -rf build || true
	@echo "-> Building Package"
	@${PYTHON_EXE} -m build

format:
	@echo "-> Making file Checks"
	@black src/LicenseClassifier/
	@isort src/LicenseClassifier/

test:
	@echo "-> Running Tests"
	@cd src; python3 -m unittest discover

check:
	@echo "-> Run pycodestyle (PEP8) validation"
	@pycodestyle --max-line-length=88 --exclude=lib,thirdparty,docs,bin,migrations,settings,data,pipelines,var .
	@echo "-> Run isort imports ordering validation"
	@isort --check-only .
	@echo "-> Run black validation"
	@black --check .