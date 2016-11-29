all: 1-single-fork-and-print \
	2-multiple-fork-and-print \
	3-single-fork-with-wait-and-print \
	4-multiple-fork-with-late-wait-and-print

1-single-fork-and-print: 1-single-fork-and-print.o fun.o
2-multiple-fork-and-print: 2-multiple-fork-and-print.o fun.o
3-single-fork-with-wait-and-print: 3-single-fork-with-wait-and-print.o fun.o
4-multiple-fork-with-late-wait-and-print: 4-multiple-fork-with-late-wait-and-print.o fun.o

%.ps: %.c 
	enscript -E --color -f Courier10 $< -o $@

%.pdf: %.ps
	ps2pdf $< 

pdf: 1-single-fork-and-print.pdf \
	2-multiple-fork-and-print.pdf \
	3-single-fork-with-wait-and-print.pdf \
	4-multiple-fork-with-late-wait-and-print.pdf

clean:
	rm -f *~ *.o

cleaner: clean
	rm -f 	1-single-fork-and-print \
		2-multiple-fork-and-print \
		3-single-fork-with-wait-and-print \
		4-multiple-fork-with-late-wait-and-print
