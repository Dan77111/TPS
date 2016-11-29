#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int is_prime(int n) {

  int top, i;

  if (n < 2)  return 0;
  if (n == 2) return 1;

  top = sqrt(n);

  for (i=2; i<top+1; ++i) 
    if ((n % i) == 0) 
      return 0;
  return 1;
}

int main(int argc, char *argv[])
{
  int top;
  int i;

  top = atoi(argv[1]);

  for (i=2; i<top+1; ++i) {
    if (is_prime(i)) {
      printf("%d\n", i);
    }
  }
  return 0;
}
