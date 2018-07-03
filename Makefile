build-docker:cleanup
	docker build -t viniciusgava/portaldorh-holerite-download:latest .

publish-image:
	docker push viniciusgava/portaldorh-holerite-download:latest

cleanup:
	rm -rf src/local/credentials.py
	rm -rf src/local/settings.py
	find . -name "__pycache__" -exec rm -rf "{}" \;
	find . -name "*.pyc" -exec rm -rf "{}" \;

validate-cleanup:
	ls -la src/local/credentials.py
	ls -la src/local/settings.py
	find . -name "__pycache__"
	find . -name "*.pyc"

prepare-local:
	cp src/local/credentials.py.dist src/local/credentials.py
	cp src/local/settings.py.dist src/local/settings.py
	pip3 install selenium
