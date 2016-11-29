#! /usr/bin/env python
import sys
import os

def char_count(filename):
    with open(filename, "rb") as file:
        return len(file.read())

def main(files):

    for f in files:
        print ("%d" % char_count(f))

    return 0

if __name__ == '__main__':

    args = sys.argv[1:]
    sys.exit(main(args))
    
