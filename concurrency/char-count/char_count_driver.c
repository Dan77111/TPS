#include <stdio.h>
#include <stdlib.h>
#include "char_count.h"

int main(int argc, char *argv[])
{ 
  int count;

  count = char_count(argv[1]);
  printf("%d\n", count);
  exit(count < 0);
}
