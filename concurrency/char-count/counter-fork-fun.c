/* 
   Esempio di fork di child multipli che eseguono una stessa funzione
   'char_count' che accetta (quindi niente exec).  La funzione accetta
   il nome di un file e ne conta i caratteri. Il risultato viene
   passato da child a parent via pipe (unica possibilità). Il parent
   fa una wait subito dopo la fork, invece di farle tutte alla fine
   (che credo sia un'altra possibilità).
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>             /* fork */
#include <sys/wait.h>           /* wait */
#include "char_count.h"

void write_count(char *fn) {

  printf("%d\n", char_count(fn));
}

int read_count(void) {

  int count;
  scanf("%d", &count);
  return count;
}

int main(int argc, char *argv[])
{ 
  pid_t pid;
  int i;

  for (i=1; i<argc; i++) {

    int tube[2];
    pipe(tube);

    pid = fork();
    if (pid == 0) {             /* child */
      
      dup2(tube[1], 1);
      write_count(argv[i]);
      exit(0);
    } else {                    /* parent */
      
      dup2(tube[0], 0);
      waitpid(pid, NULL, 0);
      printf("parent: %d child: %d count: %6d file: %s\n", 
             getpid(), pid, read_count(), argv[i]);
    }
  }
  exit(0);
}

  
  
