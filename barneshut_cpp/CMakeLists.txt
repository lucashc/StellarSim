cmake_minimum_required(VERSION 3.10)

project(StellarSim)

add_executable(Sim sim.cpp)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

enable_testing()
add_test(MemoryCheck valgrind --error-exitcode=33 ./Sim)