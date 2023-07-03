VERSION_HASH ?= $(shell git fetch && git describe --tags --always | sed 's/-/./g')
TEST_PORT = 8999
BASE_DELAY = 10
RANDOM_DELAY = 10

version:
	@git fetch
	@echo $(shell git describe --tags --always | sed 's/-/./g')


docker-build:
	docker build -t python-stratagems .

docker-run:
	docker run -d -p ${TEST_PORT}:${TEST_PORT} -e PORT=${TEST_PORT} -e BASE_DELAY=${BASE_DELAY} -e RANDOM_DELAY=${RANDOM_DELAY} --name python-stratagems python-stratagems

docker-down:
	docker stop python-stratagems
	docker rm python-stratagems

