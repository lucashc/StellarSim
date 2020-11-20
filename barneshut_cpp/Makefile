CC = g++
CFLAGS = -Wall -g

clean: 
	rm -Rf ./build
	rm -f cppsim/cppsim.cpp
	rm -f test.elf
	rm -f *.so
	rm -f *.pyd

build_cython:
	python3 setup.py build_ext --inplace

tests = $(wildcard tests/*.cpp)
tests_targets = $(notdir $(patsubst %.cpp,%.elf,$(tests)))
$(tests_targets): $(tests)
	$(CC) $(CFLAGS) $< -o build/$@

build_test: $(tests_targets)

build: build_cython build_test

test: build
	python3 tests/pytest.py
