RENDER = ./bin/render.py

.PHONY: chords

all: chords html

html: index.html

%.html: templates/%.tmpl templates/base.tmpl
	$(RENDER) `basename $<` > $@

chords:
	(cd hug-chords && git pull)
	$(MAKE) -C hug-chords
	rsync -av --delete hug-chords/pdfs .

upload:
	git add --all pdfs
	git add *.html
	git commit -m "Commit for upload on `date`"
	git push
