clean: 
	rm -Rf ./build
	rm -f nbody.cpp
build_cython:
	python3 setup.py build_ext --inplace

build: build_cython

test: build
	python3 test.py
