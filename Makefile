venv: venv/bin/activate

venv/bin/activate: requirements.txt
	python3 -m venv venv
	. venv/bin/activate; python3 -m pip install -Ur requirements.txt
	touch venv/bin/activate
clean:
	rm -rf venv
	find -iname "*.pyc" -delete
	find -iname "__pycache__" -delete

