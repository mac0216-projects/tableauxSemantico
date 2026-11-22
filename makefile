.PHONY: test 

#-------------------------------------------------------------------------------

test:
	@PYTHONPATH=src python -m unittest discover -s src/tests -p "test_*.py"

#-------------------------------------------------------------------------------

clean:
	@rm -rf $(find src/ -type d -name "__pycache__")