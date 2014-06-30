.PHONY: chords

all: chords

chords:
	(cd hug-chords && git pull)
	$(MAKE) -C hug-chords
	rsync -av --delete hug-chords/pdfs .

upload:
	git add --all pdfs
	git commit -m "Commit for upload on `date`"
	git push
