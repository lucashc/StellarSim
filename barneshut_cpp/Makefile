CC = g++
CFLAGS = -Wall -g -pthread

clean: 
	rm -Rf ./build
	rm -f cppsim_source/cppsim.cpp
	rm -f test.elf
	rm -f *.so
	rm -f *.pyd
	rm -f a.out gmon.out analysis.txt

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

profile:
	$(CC) $(CFLAGS) -pg archive/test.cpp
	./a.out
	gprof ./a.out gmon.out > analysis.txt

docs: build_cython
	pydoc -w cppsim