#proxy:="--proxy=129.104.242.2:8080"

.PHONY: depends install runserver 

venv:
	virtualenv --python=python3 venv

key:
	cat /dev/urandom | tr -d -c "[a-zA-Z0-9]" | head -c 50 > .keys/secret.key

depends: venv
	. venv/bin/activate; \
	pip3 install -r requirements.txt $(proxy)

install: depends key
	. venv/bin/activate; \
	python3 manage.py collectstatic --noinput; \
	python3 manage.py migrate

runserver: install
	. venv/bin/activate; \
	    python3 manage.py runserver 0.0.0.0:8000

migrate:
	. venv/bin/activate; \
	python3 manage.py makemigrations; \
	python3 manage.py migrate

