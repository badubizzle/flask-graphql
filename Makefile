
TESTS_DIR = ./flaskgql/test/tests/*.py

test:; @for f in ${TESTS_DIR};\
 do echo "Running test $${f}";\
  pytest -s $${f}; done

db-init:;FLASK_APP=flaskgql/main.py flask db init
db-migrate:;FLASK_APP=flaskgql/main.py flask db migrate
db-upgrade:;FLASK_APP=flaskgql/main.py flask db upgrade
run:; python3 -m flaskgql.main
