PYTHON_EXE?=python3
upload:
	@echo "-> Clearing Redundant Build Files"
	@rm -rf dist || true
	@rm -rf build || true
	@echo "-> Building Package"
	@${PYTHON_EXE} -m build
	@echo "-> Uploading to Pip"
	@twine upload dist/*

