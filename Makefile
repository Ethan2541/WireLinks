run:
	python src/main.py

setup_mac:
	pip install -r requirements.txt
	brew install python-tk

setup_linux:
	pip install -r requirements.txt
	sudo apt-get install python-tk

clean:
	rm -f src/__pycache__