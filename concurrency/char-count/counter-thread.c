#include <stdio.h>              /* printf */
#include <stdlib.h>             /* exit */
#include <unistd.h>             /* sleep */
#include <pthread.h>            /* pthread_XXX */
#include "char_count.h"

typedef struct thread_data {

  pthread_t thread;
  char *fn;
  int count;
} thread_data_t;

void print_thread_data(thread_data_t *tdp) {

  printf("%6d %s\n", tdp->count, tdp->fn);
}

void *count(void *arg) {

  thread_data_t *tdp = (thread_data_t *) arg;

  tdp->count = char_count(tdp->fn);
  pthread_exit((void *)tdp);
}

int main(int argc, char *argv[])
{ 
  int i;
  thread_data_t *threads;

  argc--;
  argv++;

  threads = (thread_data_t *) malloc(argc * sizeof(thread_data_t));
  if (threads == NULL) {

      fprintf(stderr, "malloc failed.\n");
      exit(1);    
  }
  for (i=0; i<argc; i++) {

    thread_data_t *tdp = &threads[i];

    tdp->fn = argv[i];
    if (pthread_create(&(tdp->thread), NULL, &count, tdp)) {
      
      fprintf(stderr, "pthread_create failed.\n");
      exit(1);
    }
  }
  for (i=0; i<argc; i++) {

    thread_data_t *tdp = &threads[i];

    if (pthread_join(tdp->thread, NULL)) {

      fprintf(stderr, "join on thread %d failed.\n", i);
      exit(1);
    }
    print_thread_data(tdp);
  }
  exit(0);
}
