build-docker:cleanup
	docker build --no-cache -t viniciusgava/portaldorh-holerite-download:latest .

publish-image:
	docker push viniciusgava/portaldorh-holerite-download:latest

cleanup:
	rm -rf src/settings/local.py
	find . -name "__pycache__" -exec rm -rf "{}" \;
	find . -name "*.pyc" -exec rm -rf "{}" \;

validate-cleanup:
	ls -la src/settings/local.py
	find . -name "__pycache__"
	find . -name "*.pyc"

prepare-local:
	cp src/settings/local.py.dist src/settings/local.py
	pip3 install selenium requests
