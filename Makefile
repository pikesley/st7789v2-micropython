default: format test clean

push:
	python -m mpremote cp -r *py :
	python -m mpremote cp -r lib :
	python -m mpremote cp -r conf :

connect:
	python -m mpremote

mount:
	python -m mpremote mount .

format:
	ruff format
	ruff check --fix

clean:
	@find . -depth -name __pycache__ -exec rm -fr {} \;
	@find . -depth -name .ruff_cache -exec rm -fr {} \;
	@find . -depth -name .pytest_cache -exec rm -fr {} \;

test: export TEST = 1
test:
	python -m pytest \
		--random-order \
		--verbose \
		--capture no \
		--exitfirst \
		--last-failed

nuke:
	python -m esptool \
		--chip esp32c3 \
		erase_flash

flash:
	python -m esptool \
		--chip esp32c3 \
		write_flash \
		0x0 \
		../firmware/c3-current

reinstall: nuke flash push connect
