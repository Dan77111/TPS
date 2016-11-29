all: sleeping-barber_ast pdf

sleeping-barber_ast: sleeping-barber_ast.c
	gcc -pthread -o $@ $<

pdf: sleeping-barber_ast.pdf sleeping-barber.pdf sleeping-barber-doc.pdf

%.pdf: %.tex
	pdflatex --shell-escape $<
	pdflatex --shell-escape $<
%.pdf: %.ps 
	ps2pdf $<
%.ps: %.c
	enscript -E --color -o $@ $<
%.ps: %.py
	enscript -E --color -o $@ $<
clean:
	rm -f *~ *.o *.ps
	rm -f test.out
	luke-clean-tex
	rm -f *.tex

cleaner: clean
	rm -f sleeping-barber_ast
	rm -f *.pdf

test: sleeping-barber_ast
	./$< 2>&1 > test.out
