# Requires NPM installation
build-frontend :
	cd front;\
	npm install;\
	npm run build
	-rm -r diweir/res/front
	mv front/out diweir/res/front

# Not yet implemented
run-tests :
	echo Running tests
	cd diweir/res/frontend
	npm install --save-dev jest
	npm run test

# Run this only after a NPM and PIP install run
run-checks:
	cd front;\
	npm run owasp
	~/Documents/install/dependency-check/bin/dependency-check.sh --project DIWEIR --scan $(pip show diweir | grep Location: | cut -d ' ' -f 2) --out ./reports/dependency -f HTML --enableExperimental --log ./reports/dependency/diweir.log

# Requires PIP, cleans up first before installing.
install : build-frontend
	pip uninstall diweir
	pip install .

# Pre-requisite are Anaconda and NPM installation and availability as a CLI utility
dev-setup:
	conda env create
	cd front; npm i

dev-install: build-frontend
	pip install -e .