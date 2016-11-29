#include <stdio.h>              /* printf */
#include <stdlib.h>             /* exit */
#include <unistd.h>             /* sleep */
#include <pthread.h>            /* pthread_XXX */
#include <time.h>
#include <semaphore.h>

/* shared variables */
int shared_counter = 0;
sem_t counter_semaphore;

/* program options */
int max_milli_sleep = 100;
int use_semaphores = 0;

int sleep_milli(int milli) {
  struct timespec ts;
  ts.tv_sec = milli/1000;
  ts.tv_nsec = (milli % 1000) * 1000000;
  nanosleep(&ts, NULL);
}

int sleep_max_milli(int max_milli) {
  if (max_milli > 0) sleep_milli(rand() % max_milli);
}

void *work(void *foo) {

  int old;

  if (use_semaphores) sem_wait(&counter_semaphore);
  old = shared_counter;
  sleep_max_milli(max_milli_sleep);
  shared_counter++;
  if ((old+1) != shared_counter) {
    
    fprintf(stderr, 
            "Error in shared counter old: %d new: %d!\n",
            old, shared_counter);
    exit(1);
  }
  if (use_semaphores) sem_post(&counter_semaphore);
}

int main(int argc, char *argv[])
{ 
  int i;
  int thread_count = 5;

  pthread_t *threads;

  argc--;
  argv++;

  if (argc > 0) thread_count = atoi(argv[0]);
  if (argc > 1) max_milli_sleep = atoi(argv[1]);
  if (argc > 2) use_semaphores = 1;

  threads = (pthread_t *) malloc(thread_count * sizeof(pthread_t));
  if (threads == NULL) {
      fprintf(stderr, "pthread_join failed!\n");
      exit(1);
  }

  sem_init(&counter_semaphore, 
           0,  /* 0 means threads share semaphore */
           1); /* sem initial value */

  for (i=0; i<thread_count; i++) {


    int ret = pthread_create(&threads[i], NULL, &work, NULL);
    if (ret) {

      fprintf(stderr, 
              "pthread_create failed at call number %d.\n", i);
      perror("");
      exit(1);
    }
      /*
      EAGAIN Insufficient  resources  to  create another thread, or a system-imposed limit on the number of threads was encountered.  The
              latter case may occur in two ways: the RLIMIT_NPROC soft resource limit (set via setrlimit(2)), which limits the  number  of
              process  for  a  real  user  ID,  was  reached;  or  the kernel's system-wide limit on the number of threads, /proc/sys/ker‐
              nel/threads-max, was reached.

       EINVAL Invalid settings in attr.

       EPERM  No permission to set the scheduling policy and parameters specified in attr.
      */
  }
  for (i=0; i<thread_count; i++) {

    if (pthread_join(threads[i], NULL)) {

      fprintf(stderr, 
              "pthread_join failed on thread %d!\n", i);
      exit(1);
    }
  }
  sem_destroy(&counter_semaphore);

  printf("OK: %d\n", shared_counter);
  exit(0);
}
