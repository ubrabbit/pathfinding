#!/bin/bash

g++ -g -Wall -O3 -std=c++11 -Wextra -c -fpic -c Point.cpp -o Point.o
g++ -g -Wall -O3 -std=c++11 -Wextra -c -fpic -c Node.cpp -o Node.o
g++ -g -Wall -O3 -std=c++11 -Wextra -c -fpic -c Grid.cpp -o Grid.o
g++ -g -Wall -O3 -std=c++11 -Wextra -c -fpic -c PathFinding.cpp -o PathFinding.o
g++ -g -Wall -O3 -std=c++11 -Wextra -c -fpic -c test.cpp -o test.o

g++ Point.o Node.o Grid.o PathFinding.o test.o -o test
rm Point.o Node.o Grid.o PathFinding.o test.o

echo "build success"
echo
./test
echo
echo "run finished"
