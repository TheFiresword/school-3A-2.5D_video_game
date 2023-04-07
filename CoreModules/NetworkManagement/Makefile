CC = gcc
CFLAGS = -Wall -g
SRCDIR = src_new
OBJDIR = objects_new
INCDIR = headers
BINDIR = bin

# List of source files located in different subfolders
SRCS = $(wildcard $(SRCDIR)/**/*.c $(SRCDIR)/*.c)

# List of object files that will be created in the obj/ directory
OBJS = $(patsubst $(SRCDIR)/%.c,$(OBJDIR)/%.o,$(SRCS))

# Include directories
INCLUDES = -I$(INCDIR)

# Target to build the executable
$(BINDIR)/myprogram: $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

# Rule to compile each C++ source file into an object file
$(OBJDIR)/%.o: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $<

# Phony targets
.PHONY: clean

# Clean up object files and executable
clean:
	rm -f $(OBJDIR)/*/*.o $(OBJDIR)/*.o $(BINDIR)/myprogram

clean_before_make:
	make clean
	make

total:
	make clean
	make
	clear 
	./bin/myprogram