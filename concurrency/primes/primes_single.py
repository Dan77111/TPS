#! /usr/bin/env python
import sys
import os
import math

def is_prime(n):

    if n < 2:  return False
    if n == 2: return True
            
    top = int(math.sqrt(n))
    for i in range(2, top+1):
        if n % i == 0:
            return False
    return True
        
if __name__ == '__main__':

    args = sys.argv[1:]
    if not args:
        sys.exit(1)
    top = int(args[0])
    for n in range(top):
        if is_prime(n):
            print n


    
