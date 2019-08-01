# the directory which contains all the source files
SOURCE_DIR := ./src
# all the source files
SOURCES := $(wildcard $(SOURCE_DIR)/*.cpp)
# the directory which contains all the compiled objects
OBJECT_DIR := ./obj
# Object files to either reference or create
OBJECTS := $(patsubst $(SOURCE_DIR)/%.cpp,$(OBJECT_DIR)/%.o,$(SOURCES))
# The executable file that will be created at the end
EXEC := Connect4Game.out
# The flags to use for compilation
FLAGS := -Wall -std=c++11
# The code compiler to use for compilation
CC := g++

all: $(EXEC)

$(EXEC): $(OBJECTS)
	$(CC) $(FLAGS) $(OBJECTS) -o $@
$(OBJECT_DIR)/%.o: $(SOURCE_DIR)/%.cpp
	$(CC) -g -c $< -o $@

obj: $(OBJECTS)
$(OBJECT_DIR)/%.o: $(SOURCE_DIR)/%.cpp
	$(CC) -g -c $< -o $@

clean:
	rm -f $(EXEC)
	rm -f $(OBJECT_DIR)/*.o