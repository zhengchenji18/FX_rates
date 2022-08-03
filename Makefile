run:
	python application.py

install:
    pip install -r requirements.txt

lint:
	pylint application.py