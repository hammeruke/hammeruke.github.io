RENDER = ./bin/render.py

.PHONY: chords

all: chords html

html: index.html songs.html

%.html: templates/%.tmpl templates/base.tmpl
	$(RENDER) `basename $<` > $@

chords:
	(cd hug-chords && git pull)
	$(MAKE) -C hug-chords
	rsync -av --delete hug-chords/pdfs .
	mogrify  -format png pdfs/hug-songbook.pdf
	mogrify -background '#ffffff' -flatten pdfs/*.png


upload:
	git add --all pdfs
	git add *.html
	git commit -m "Commit for upload on `date`"
	git push
