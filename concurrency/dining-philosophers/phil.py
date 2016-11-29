
import threading
import random
import time
import sys

PHIL_COUNT = 5
THINKING, HUNGRY, EATING = range(3)
STATE = [THINKING] * PHIL_COUNT
SEM_STATE = threading.Semaphore(1)

def LEFT(i):
    return (i + 1) % PHIL_COUNT

def RIGHT(i):
    return (i - 1) % PHIL_COUNT

def wait(sem):
    sem.acquire()

def signal(sem):
    sem.release()

acquire = wait
release = signal

def get_think_time(i):
  return random.random()

def get_eat_time(i):
  return random.random()

def show(s):
    sys.stderr.write(s + "\n")
    
def think(i):
  show("THINK %d" % i)
  t = get_think_time(i)
  time.sleep(t)

def eat(i):
  show("EAT %d" % i)
  t = get_eat_time(i)
  time.sleep(t)

RUN = True

def philosopher(i):

  while RUN:
      think(i)
      take_forks(i)
      eat(i)
      put_forks(i)

def put_forks(i):
    acquire(SEM_STATE)
    STATE[i] = THINKING
    test_chance(LEFT(i))
    test_chance(RIGHT(i))
    release(SEM_STATE)

TURN = [threading.Semaphore(0) for _ in range(PHIL_COUNT)]

def test_chance(i):
    if (STATE[i] == HUNGRY and
        STATE[LEFT(i)] != EATING and
        STATE[RIGHT(i)] != EATING):

        signal(TURN[i])

def take_forks(i):
    acquire(SEM_STATE)
    STATE[i] = HUNGRY
    test_chance(i)
    release(SEM_STATE)
    wait(TURN[i])

def test_chance(i):
    if (STATE[i] == HUNGRY and
        STATE[LEFT(i)] != EATING and
        STATE[RIGHT(i)] != EATING):

        STATE[i] = EATING
        signal(TURN[i])
        ii = [str(i) for i in range(PHIL_COUNT) if STATE[i] == EATING]
        s = ", ".join(ii)
        show("Eaters: %s" % s)
        if len(ii) > 2:         
            raise Exception("Cazzarola")

def main():

    tt = [threading.Thread(target=philosopher,
                           args=(i,))
                           for i in range(PHIL_COUNT)]
    for t in tt:
        t.start()

    for t in tt:
        t.join()

if __name__ == '__main__':

    main()
