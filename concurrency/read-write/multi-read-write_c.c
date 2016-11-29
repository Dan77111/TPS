#include <stdio.h>              /* printf */
#include <stdlib.h>             /* exit */
#include <unistd.h>             /* sleep */
#include <pthread.h>            /* pthread_XXX */
#include <semaphore.h>          /* sem_XXX */
#include <math.h>               /* fmod */

int writers_count = 5;
int readers_count = 3;
int items_count = 150;
int buffer_size = 8;
int *buffer;

int write_left;
int write_pos = 0;
int read_left;
int read_pos = 0;

typedef sem_t semaphore;
semaphore sem_writer;        
semaphore sem_reader;
semaphore sem_empty;
semaphore sem_full;

#define down(o) sem_wait(o)     // keep AST name 'down' 
#define up(o)   sem_post(o)     // keep AST name 'up'   

void sleep_sec(float sec) {
  struct timespec ts;

  sec *= 1000;
  ts.tv_sec = sec/1000;
  ts.tv_nsec = fmod(sec, 1000) * 1000000;
  nanosleep(&ts, NULL);
}

void sleep_between(float min, float max) {
  sleep_sec(min);
  sleep_sec(fmod(rand(), max-min));
}

int make_item() {
  sleep_between(0.1, 0.2);
  return rand() % 100;
}

int use_item(i) {
  sleep_between(0.5, 0.6);
  return rand() % 100;
}

void writer(int id) {

  while (1) {

    int c, pos;

    down(&sem_empty);
    down(&sem_writer);
    write_left --;
    pos = write_pos;
    write_pos = (write_pos + 1) % buffer_size;
    c = make_item();
    up(&sem_writer);
    fprintf(stderr, "writer %3d writing %3d at %3d count: %d",
            id, c, pos, write_left);
    buffer[pos] = c;
    up(&sem_full);
  }
}

void *writer_worker(void *arg) {
  
  writer(*(int *)arg);
  return NULL;
}

void reader(int id) {
  
  while (1) {

    int c, pos;

    down(&sem_full);
    down(&sem_reader);
    read_left --;
    pos = read_pos;
    read_pos = (read_pos + 1) % buffer_size;
    c = buffer[pos];
    fprintf(stderr, "reader %3d read    %3d at %3d count: %d",
            id, c, pos, read_left);
    buffer[pos] = -1;   
    if (c < 0) {
      fprintf(stderr, "reader %d just read -1!\n", id);
      exit(1);
    }
    up(&sem_reader);
    up(&sem_empty);
    use_item(c);
  }
}

void *reader_worker(void *arg) {
  
  reader(*(int *)arg);
  return NULL;
}

pthread_t * alloc_threads(int count) {

  pthread_t *threads;

  threads = (pthread_t *) malloc(count * sizeof(pthread_t));
  if (threads == NULL) {
      fprintf(stderr, "malloc (threads) failed!\n");
      exit(1);
  }
  return threads;
}

int main(int argc, char *argv[])
{
  pthread_t *writers;
  pthread_t *readers;

  write_left = items_count;

  sem_init(&sem_writer, 0, 1);
  sem_init(&sem_reader, 0, 1);
  sem_init(&sem_empty,  0, buffer_size);
  sem_init(&sem_full,   0, 0);

  buffer = (int *) malloc(buffer_size * sizeof(int));

  writers = alloc_threads(writers_count);
  readers = alloc_threads(readers_count);

  printf("main: writers: %d readers: %d\n", 
         writers_count, readers_count);
  return 0;
}
