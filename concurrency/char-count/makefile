all: t_char_count counter char_count_driver \
	counter-late-wait counter-thread

char_count.o: char_count.c char_count.h

t_char_count.o: t_char_count.c char_count.h
t_char_count: t_char_count.o char_count.o
	gcc $^ -o $@

counter.o: counter.c char_count.h
counter: counter.o char_count.o
	gcc $^ -o $@

char_count_driver.o: char_count_driver.c char_count.h
char_count_driver: char_count_driver.o char_count.o
	gcc $^ -o $@

counter-late-wait.o: counter-late-wait.c char_count.h
counter-late-wait: counter-late-wait.o char_count.o
	gcc $^ -o $@

counter-thread.o: counter-thread.c char_count.h
counter-thread: counter-thread.o char_count.o
	gcc $^ -pthread -o $@

%.ps: %.c 
	enscript -E --color -f Courier10 $< -o $@

%.pdf: %.ps
	ps2pdf $< 

pdf: char_count.pdf counter.pdf char_count_driver.pdf \
	counter-late-wait.pdf counter-thread.pdf
clean:
	rm -f *~ *.o *.ps *.pyc
	rm -rf __pycache__

cleaner: clean
	rm -f *.pdf
	rm -f \
	t_char_count counter \
	counter \
	char_count_driver \
	counter-late-wait \
	counter-thread

