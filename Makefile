run:
	python3 src/main.py

setup:
	- brew install pip
	- brew install python3-tk
	- sudo apt-get pip
	- sudo apt-get install python3-tk
	pip install -r requirements.txt

clean:
	- rm -rf src/__pycache__