CC = g++
CFLAGS  := -g -Wall -O3 -std=c++11 -Wextra
INCLUDE_PY = `python3.5-config --includes --libs`

code_objects = Point.o Node.o Grid.o PathFinding.o PythonInterface.o

all:	c_path clean

c_path:	$(code_objects)
	g++ $(code_objects) \
	-shared \
	${INCLUDE_PY} \
	-o c_path.so

%.o : %.cpp
	$(CC) $(CFLAGS) -fPIC -c $< -o $@ $(INCLUDE_PY)

.PHONY : clean
clean:
	-rm $(code_objects)
