PYTHON_EXE?=python3
package:
	@echo "-> Clearing Redundant Build Files"
	@rm -rf dist || true
	@rm -rf build || true
	@echo "-> Building Package"
	@${PYTHON_EXE} -m build

