PYTHON_EXE?=python3
ACTIVATE?=. bin/activate;

dev:
	@echo "-> Setting up your environment"
	@${PYTHON_EXE} -m venv .
	@${ACTIVATE} pip install -r etc/requirements.txt

package: format test
	@echo "-> Clearing Redundant Build Files"
	@rm -rf dist || true
	@rm -rf build || true
	@echo "-> Building Package"
	@${ACTIVATE} ${PYTHON_EXE} -m build

format:
	@echo "-> Making file Checks"
	@${ACTIVATE} black src/LicenseClassifier
	@${ACTIVATE} isort src/LicenseClassifier

test:
	@echo "-> Running Tests"
	@${ACTIVATE} ${PYTHON_EXE} -m unittest discover src
	
check:
	@echo "-> Run pycodestyle (PEP8) validation"
	@${ACTIVATE} pycodestyle --max-line-length=88 src/LicenseClassifier
	@echo "-> Run isort imports ordering validation"
	@${ACTIVATE} isort --check-only src/LicenseClassifier
	@echo "-> Run black validation"
	@${ACTIVATE} black --check src/LicenseClassifier