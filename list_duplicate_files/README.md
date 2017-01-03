# Introduction
This is a basic helper tool that list duplicate files within a specified path.

This simple script is developed in Java 8 by me, Gan Tu.

# Specfic Details
By default, the tool lists the duplicate files if it deletes duplicate files.

Note that when prompted for a path name, it has to be the complete path name
for the directory. For example, "/Users/Michael-Tu/messy/".

You can obtain the complete path name by typing into your terminal the following command, under the directory you want to clean.

```
$ pwd
```

# Running the script
To run the tool, you can simply compile the tool using:

```
$ javac ListDuplicate.java
$ java ListDuplicate
```

or you can alternatively use the supplied Makefile:

```
$ make # this command compiles the java files
$ make check # this command runs the file
```

After running, the terminal should prompt you to enter a path, where you shall supply
the path name to the directory under which you want to clean duplicate files.

The terminal will keep prompting you for a path name until the given path is valid.

# Clean Up
You can run the following line to quickly delete compiled java class files after use.

```
$ make clean
```

