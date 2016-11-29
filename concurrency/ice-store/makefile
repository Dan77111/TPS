all: ice-store.pdf ice-store-new.pdf ice-store-doc.pdf ice-store_raw.pdf

%.pdf: %.ps 
	ps2pdf $<

ice-store_raw.ps: ice-store_raw.py
	enscript -L 50 -2r -o $@ -E --color -C -f Courier9 $<

%.ps: %.py
	enscript -E --color -fCourier12 -o $@ $<

ice-store-doc.pdf: ice-store-doc.tex
	pdflatex --shell-escape $<
	pdflatex --shell-escape $<

clean:
	rm -f *~ *.o *.ps
	rm -f test.out
	luke-clean-tex
	rm -f *.tex

cleaner: clean
	rm -f *.pdf

