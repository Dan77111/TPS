#include <stdio.h>
#include "char_count.h"
int char_count(char *file_name) {

  FILE *input;
  int i = 0;
  
  input = fopen(file_name, "r"); 
  if (input == NULL) {

    fprintf(stderr, "char_count: open on '%s' failed.\n", 
            file_name);
    return -1;
  }

  while (fgetc(input) != EOF) i++;
  fclose(input);
  return i;
}
