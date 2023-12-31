install:
	# install commands
	pip install --upgrade pip && pip install -r requirements.txt
format:
	# format code
	black *.py
lint:
	# pylint
	pylint --disable=R,C *.py
test:
	# pytest
	pytest videoapp/tests/test*.py
	
run:
	# run the python file
	uvicorn videoapp.main:app --port 8001 --reload
