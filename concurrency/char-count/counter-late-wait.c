/* 
   Esempio di fork di child multipli.  Il programma principale fa
   varie fork, una per ciascuno dei suoi argomenti (di argv) ed in
   ciascuna fork viene calcolato (usando più o meno direttamente una
   funzione 'char_count') il numero di caratteri nel file, che viene
   passato al processo principale usando una pipe creata prima della
   fork (e quindi condivisa). 

   La scrittura (nel figlio) viene fatta dalla funzione 'write_count',
   mentre la lettura (nel padre) viene fatta con la funzione
   'read_count'. 'write_count' lavora in modo diverso a seconda del
   valore della variabile globale `fork_function': se è 'true',
   write_count chiama direttamente char_count, altrimenti fa una execl
   del programma char_count_driver che, come si può capire dal nome,
   non è altro che un wrapper di char_count.

   In questa "versione" del programma le wait non sono fatte subito
   dopo le fork, ma bensí tutte alla fine.  In questo modo la cosa si
   complica un po' perché come connessione parent/child non basta una
   singola pipe (riciclata per ciascuna fork) ma serve un file
   descriptor (per la lettura) per ciascun figlio, quindi un vettore
   di "coppie" (child pid, read file descriptor) in cui, al return di
   ciascuna wait, "cercare" il file descriptor corretto.
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>             /* fork */
#include <sys/wait.h>           /* wait */
#include "char_count.h"

int VERBOSE = 0;

int fork_function = 0;

int write_count(char *fn) {

  if (fork_function) {
    printf("%d\n", char_count(fn));

  } else {

    char prog[] = "./char_count_driver";
    execl(prog, prog, fn, NULL);
    fprintf(stderr, "execl of %s on %s failed.\n", prog, fn);
  }
}

int read_count(void) {

  int count;
  scanf("%d", &count);
  return count;
}

typedef struct connection {

  pid_t pid;
  int read_fd;
} connection_t;

int main(int argc, char *argv[])
{ 
  pid_t pid;
  int i, j;
  int waiting;
  connection_t *tubes;

  argc--;
  argv++;

  tubes = (connection_t *) malloc(argc * sizeof(connection_t));

  for (i=0; i<argc; i++) {

    int tube[2];
    pipe(tube);

    pid = fork();
    if (pid == 0) {             /* child */

      dup2(tube[1], 1);           /* connect stdout */
      write_count(argv[i]);       /* write count to pipe */

      exit(0);                  
    } else {

      tubes[i].pid = pid;
      tubes[i].read_fd = tube[0];
    }
  }
  for (i=0; i<argc; i++) {
    
    int status;
    int pid = waitpid(0, &status, 0);
    int count;

    for (j=0; j<argc; j++)      /* find right tube for pid */
      if (tubes[j].pid == pid) 
        dup2(tubes[i].read_fd, 0);

    count = read_count();
    if (count < 0) {
      printf("parent: %d child: %d count on %s failed\n", 
             getpid(), pid, argv[i]);
    } else {
      if (VERBOSE) {
          printf("parent: %d child: %d count: %6d file: %s\n", 
                 getpid(), pid, count, argv[i]);
        } else {
          printf("%d %s\n", count, argv[i]);
      }
    }
  }
  exit(0);
}
