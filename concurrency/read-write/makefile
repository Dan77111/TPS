all: 	multi-read-write.pdf multi-read-write_oop.pdf \
	multi-read-write_c.pdf read-write.pdf \
	read-write-doc.pdf multi-read-write_raw.pdf \
	read-write_forecast.pdf read-write_dia.pdf \
	multi-read-write_queue.pdf

multi-read-write_raw.ps: multi-read-write_raw.py
	enscript -L 50 -2r -o $@ -E --color -C -f Courier9 $<

%.pdf: %.ps
	ps2pdf $<

%.pdf: %.tex
	pdflatex --shell-escape $<
	pdflatex --shell-escape $<

%.ps: %.py
	enscript -E --color -fCourier12 $< -o $@

%.ps: %.c
	enscript -E --color -fCourier12 $< -o $@

clean:
	rm -f *~ *.ps *.tex *.pyg
	luke-clean-tex

cleaner: clean
	rm -f *.pdf
