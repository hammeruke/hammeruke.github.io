RENDER = ./bin/render.py
PDFS=$(wildcard pdfs/hug/*.pdf)
PNGS=$(patsubst pdfs/%.pdf,pngs/%.png,$(PDFS))

.PHONY: newsongs pdfs touch

all: pdfs pngs html

html: index.html songs.html

%.html: templates/%.tmpl templates/base.tmpl $(RENDER)
	$(RENDER) `basename $<` > $@

pdfs:
	$(MAKE) PDFDIR=`pwd`/pdfs -C hug-chords

pngs: $(PNGS)

pngs/%.png: pdfs/%.pdf
	mkdir -p `dirname $@`
	convert $< -format png -background '#ffffff' -flatten $@

newsongs:
	(cd hug-chords && git checkout master && git pull)
	make

upload:
	git add --all pdfs pngs
	git add *.html
	git add hug-songs
	git commit -m "Commit for upload on `date`"
	git push

touch:
	find pdfs -name "*.pdf" -exec touch {} \;
	sleep 1
	find pngs -name "*.png" -exec touch {} \;
