all: primes_single

primes_single: primes_single.c
	gcc $< -lm -o $@

clean:
	rm -f *~ *.o primes_single
	rm -f a b 

test: primes_single
	./primes_single    1000 > a
	./primes_single.py 1000 > b
	diff a b 


