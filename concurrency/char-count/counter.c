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
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>             /* fork */
#include <sys/wait.h>           /* wait */
#include "char_count.h"

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

int main(int argc, char *argv[])
{ 
  pid_t pid;
  int i;

  for (i=1; i<argc; i++) {

    int tube[2];
    pipe(tube);

    pid = fork();
    if (pid == 0) {             /* child */

      dup2(tube[1], 1);           /* connect stdout */
      write_count(argv[i]);       /* write count to pipe */

      exit(0);                  
    } else {                    /* parent */

      int count;
      dup2(tube[0], 0);         /* connect stdin */
      waitpid(pid, NULL, 0);    /* read count from pipe */
      count = read_count();

      if (count < 0) 
        printf("parent: %d child: %d count on %s failed\n", 
             getpid(), pid, argv[i]);
      else
        printf("parent: %d child: %d count: %6d file: %s\n", 
               getpid(), pid, count, argv[i]);
    }
  }
  exit(0);
}

  
  
