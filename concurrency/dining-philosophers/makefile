all: pdf

pdf: 	dining-philosophers_ast.pdf \
	dining-philosophers.pdf \
	dining-philosophers-doc.pdf

dining-philosophers_ast: dining-philosophers_ast.c
	gcc -pthread -o $@ $<

%.pdf: %.ps 
	ps2pdf $<
	ps2pdf $<
%.ps: %.c
	enscript -E --color -o $@ $<
%.ps: %.py
	enscript -E --color -o $@ $<

%.pdf: %.tex
	pdflatex --shell-escape $<
	pdflatex --shell-escape $<

clean:
	rm -f *~ *.o *.ps
	rm -f test.out
	luke-clean-tex
	rm -f *.tex

cleaner: clean
	rm -f dining-philosophers_ast
	rm -f *.pdf

test: dining-philosophers_ast
	./$< 2>&1 > test.out
