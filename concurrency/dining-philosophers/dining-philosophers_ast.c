/* 
   Esempio di soluzione del classico prolema dei cinque filosofi a
   cena. La soluzione è quella descritta nel Tanenbaum (AST), a parte
   alcuni cambi docuti alla piattaforma, alcune aggiunte di parti
   mancanti (es: think, eat e il main!) e la parte di "logging" per
   cercare di capire se e come funziona il tutto.
 */

// Manini: ----------------------------------------------------

#include <stdio.h>              /* printf */
#include <stdlib.h>             /* exit */
#include <unistd.h>             /* sleep */
#include <pthread.h>            /* pthread_XXX */
#include <semaphore.h>          /* sem_XXX */

// AST (salvo modifiche) --------------------------------------

#define N 5
#define LEFT  (i-1) % N
#define RIGHT (i+1) % N
#define THINKING 0
#define HUNGRY   1
#define EATING   2
typedef sem_t semaphore;        // AST: typedef int semaphore;
semaphore mutex;           // AST: mutex = 1. Qui: up in main! 
semaphore s[N];                 // sem_init in main 
int state[N];
#define down(o) sem_wait(o)     // keep AST name 'down' 
#define up(o)   sem_post(o)     // keep AST name 'up'   

// Manini: logging -------------------------------------------

char state_names[] = "THE";
int mill_sleep_eat = 10;
int mill_sleep_think = 100;

// AST (salvo modifiche) -------------------------------------

void philosopher(int i);
void think(int i);              /* AST: void think(void) */
void take_forks(int i);
void eat(int i);                /* AST: viod eat(void) */
void put_forks(int i);
void test(int i);

// Manini: logging --------------------------------------------

void *worker(void *arg);
void sleep_milli(int milli);
void sleep_max_milli(int max_milli);
void print_eaters(void);

// AST --------------------------------------------------------

void philosopher(int i) {

  int steps = 100;
  while (steps--) {             /* AST: while (1) */
    think(i);
    take_forks(i);
    eat(i);
    put_forks(i);
  }
}

void think(int i) {             /* AST: empty function */
  printf("phil %d THINKING\n", i);
  sleep_max_milli(mill_sleep_think);
};

void eat(int i) {               /* AST: empty function */
  printf("phil %d EATING\n", i);
  print_eaters();
  sleep_max_milli(mill_sleep_eat);
};

// MUTEX and SEMAPHORES -----------------------------------

void test(int i) {
  
  if (state[i]     == HUNGRY &&
      state[LEFT]  != EATING &&
      state[RIGHT] != EATING) {
    
    state[i] = EATING;
    up(&s[i]);     /* called by myself AND by +- 1  */
  }
}

void take_forks(int i) {

  down(&mutex);
  state[i] = HUNGRY;
  printf("phil %d HUNGRY\n", i); /* Manini */
  test(i);
  up(&mutex);
  down(&s[i]);  /* called ONLY by myself */
}

void put_forks(int i) {

  down(&mutex);
  state[i] = THINKING;
  test(LEFT);
  test(RIGHT);
  up(&mutex);
}

// Manini: --------------------------------------------

void *worker(void *arg) {
  
  philosopher(*(int *)arg);
  return NULL;
}

void print_eaters(void) {

  int i;
  int c = 0;
  down(&mutex);
  printf("states: ");
  for (i=0;i<N;i++) {
    
    printf(" %c", state_names[state[i]]);
    if (state[i] == EATING) c++;
  }
  printf("\n");
  if (c > 2) {

    fprintf(stderr, "ERROR: more than one phil eating!\n");
  }
  if (c > 0) {
    printf ("    phils eating: ");
    for (i=0;i<N;i++) {
      
      if (state[i] == EATING) printf(" %d", i);
    }
    printf("\n");
  }
  up(&mutex);
}

void sleep_milli(int milli) {
  struct timespec ts;
  ts.tv_sec = milli/1000;
  ts.tv_nsec = (milli % 1000) * 1000000;
  nanosleep(&ts, NULL);
}

void sleep_max_milli(int max_milli) {
  if (max_milli > 0) sleep_milli(rand() % max_milli);
}

// Manini: thread ---------------------------------------------- 

pthread_t * alloc_threads(int count) {

  pthread_t *threads;

  threads = (pthread_t *) malloc(count * sizeof(pthread_t));
  if (threads == NULL) {
      fprintf(stderr, "malloc (threads) failed!\n");
      exit(1);
  }
  return threads;
}

void free_threads(pthread_t *threads) {

  free(threads);
}

void run_threads(pthread_t *threads, int count, 
                 void *(*worker)(void *)) {

  int i;
  for (i=0; i<count; i++) {
    
    int ret = pthread_create(&threads[i], NULL, 
                             worker, (void *)&i);
    sleep(1);
    // printf("run_threads: starting thread %d\n", i);
    if (ret) {
      
      fprintf(stderr, 
              "pthread_create failed at call number %d.\n", i);
      perror("");
      exit(1);
    }
  }
}

void join_threads(pthread_t *threads, int count) {

  int i;
  for (i=0; i<count; i++) {

    if (pthread_join(threads[i], NULL)) {

      fprintf(stderr, 
              "pthread_join failed on thread %d!\n", i);
      exit(1);
    }
  }
}

void init_semaphores(sem_t *semaphores, int count, int value) {

  int i;
  for (i=0; i<N; i++) {
    sem_init(&semaphores[i], 
             0,       /* shared between threads */
             value);      /* initial value */
  }
}

int main(int argc, char *argv[])
{
  pthread_t *threads;

  printf("MAIN: starting with %d philosophers\n", N);
  up(&mutex);
  init_semaphores(s, N, 1);
  threads = alloc_threads(N);
  run_threads(threads, N, &worker);
  join_threads(threads, N);
  free_threads(threads);
  return 0;
}
