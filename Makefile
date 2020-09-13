all:
	echo All done!

test:
	./spidertube.py

run:
	./spidertube.py | tee `date +%Y-%m-%d_%H-%M-%S.log`
