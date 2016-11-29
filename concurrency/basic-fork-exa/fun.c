#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include "fun.h"

void get_opt(int argc, char *argv[], 
             int *sleep_child, 
             int *sleep_parent,
             int *do_wait) {

  int opt;
  while ((opt = getopt(argc, argv, "-c:-p:w:")) != -1) {

    switch (opt) {
    case 'c':
      if (sleep_child) *sleep_child = atoi(optarg);
      break;
    case 'p':
      if (sleep_parent) *sleep_parent = atoi(optarg);
      break;
    case 'w':
      if (do_wait) *do_wait = atoi(optarg);
      break;
    default: /* '?' */
      continue;
    }
  }
}
