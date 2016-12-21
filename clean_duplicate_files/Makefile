SHELL = bash

JFLAGS = -g -Xlint:unchecked -encoding utf8

SRCS = $(wildcard *.java)

CLASSES = $(SRCS:.java=.class)

# Tell make that these are not really files.
.PHONY: clean default check 

default: compile

compile: $(CLASSES)


$(CLASSES): sentinel

sentinel: $(SRCS)
	javac $(JFLAGS) $(SRCS)
	touch $@

# Run Tests.
check: compile
	java CleanDuplicates

# Find and remove all *~ and *.class files.
clean:
	$(RM) sentinel *.class *~ 

