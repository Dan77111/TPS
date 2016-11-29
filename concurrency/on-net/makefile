SRC := $(wildcard *.py)
PDF := $(patsubst %.py, %.pdf, $(SRC))

all: test_multi

%.ps: %.py
	enscript -E --color -fCourier10 $< -o $@

%.pdf: %.ps
	ps2pdf $<

pdf: $(PDF)

test_multi:
	python multi.py -s &
	python multi.py -c &
	python multi.py -c &
	python multi.py -c &
	python multi.py -c &
	python multi.py -c &

clean:
	rm -f *~ *pyc

cleaner: clean
	rm -f *.pdf
