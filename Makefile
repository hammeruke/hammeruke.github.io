RENDER = ./bin/render.py

.PHONY: chords

all: chords html

html: index.html songs.html

%.html: templates/%.tmpl templates/base.tmpl
	$(RENDER) `basename $<` > $@

chords:
	(cd hug-chords && git pull)
	$(MAKE) -C hug-chords
	mogrify  -format png hug-chords/pdfs/hug-songbook.pdf
	mogrify -background '#ffffff' -flatten hug-chords/pdfs/*.png
	rsync -av --delete hug-chords/pdfs .


upload:
	git add --all pdfs
	git add *.html
	git commit -m "Commit for upload on `date`"
	git push
