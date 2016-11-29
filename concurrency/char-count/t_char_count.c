#include <stdio.h>
#include <stdlib.h>
#include "char_count.h"

int main(int argc, char *argv[])
{ 
  int i, count;

  for (i=1; i<argc; i++) {
    
    count = char_count(argv[i]);
    if (i < 0) {
      
      fprintf(stderr, 
              "char_count failed on '%s'\n",
              argv[i]);
    } else {
      printf("%6d %s\n", count, argv[i]);
    }
  }
  exit(0);
}
