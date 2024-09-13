all: testall

LOCKFILE=/tmp/up.run
PULL=missing

testall:
	for i in tests/*.py; do \
	  python $$i; \
	done

test: python-init
	pipenv run python $(FILE)

up: $(LOCKFILE)

down:
	docker compose -p test down --rmi local
	make clean

$(LOCKFILE):
	docker compose -p test -f compose.yml -f compose_test.yml up --pull $(PULL) --quiet-pull -d | tee $(LOCKFILE)
	sleep 5
	@echo "Waiting for db to be ready..."
	sh -c "while ! docker exec --env-file=./env.txt $$(docker compose -p test ps -q db) /usr/local/bin/healthcheck.sh; do sleep 1; done"
	[ -n $${GITHUB_ACTIONS} ] && docker compose -p test exec web sh -c 'sudo chown -R `whoami` /workspaces'

clean:
	rm -f $(LOCKFILE)


testall_in_docker: up
	docker compose -p test exec -w /workspaces web make testall
	make down

test_in_docker: up
	docker compose -p test exec -w /workspaces web make test FILE=$(FILE)
	make down


python-init:
	which pipenv || pip install pipenv --break-system-packages
	pipenv install --dev -q && pipenv graph

