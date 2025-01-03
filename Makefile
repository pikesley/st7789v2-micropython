ID = $(shell basename $$(pwd))

default: format test clean

build:
	docker build \
		--build-arg ID=${ID} \
		--tag ${ID} .

run:
	docker run \
		--name ${ID} \
		--hostname ${ID} \
		--volume $(shell pwd):/opt/${ID} \
		--interactive \
		--tty \
		--rm \
		${ID} \
		bash

push:
	python -m mpremote cp -r *py :
	python -m mpremote cp -r st7789v2 :

connect:
	python -m mpremote

format:
	ruff format
	ruff check --fix

clean:
	@find . -depth -name __pycache__ -exec rm -fr {} \;
	@find . -depth -name .ruff_cache -exec rm -fr {} \;
	@find . -depth -name .pytest_cache -exec rm -fr {} \;

# test: export TEST = 1
test:
	python -m pytest \
		--random-order \
		--verbose \
		--capture no \
		--exitfirst \
		--last-failed

nuke:
	python -m esptool \
		erase_flash

flash-mini:
	python -m esptool \
		--chip esp32c3 \
		write_flash \
		0x0 \
		../esp32-firmware/c3-current

flash:
	python -m esptool \
		--chip esp32 \
		write_flash \
		0x1000 \
		../esp32-firmware/current

reinstall: nuke flash-mini push connect
