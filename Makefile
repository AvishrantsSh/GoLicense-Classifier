PYTHON_EXE?=python3
package: format
	@echo "-> Clearing Redundant Build Files"
	@rm -rf dist || true
	@rm -rf build || true
	@echo "-> Building Package"
	@${PYTHON_EXE} -m build

format:
	@echo "Making file Checks"
	@black src/LicenseClassifier/classifier.py
	@isort src/LicenseClassifier/classifier.py