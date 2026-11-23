.PHONY: test 

#-------------------------------------------------------------------------------

test:
	@PYTHONPATH=src python -m unittest discover -s src/tests -p "teste_*.py"

#-------------------------------------------------------------------------------

clean:
	@rm -rf $(find src/ -type d -name "__pycache__")

#-------------------------------------------------------------------------------
tablo:
	@PYTHONPATH=src python main.py