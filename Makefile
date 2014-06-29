.PHONY: chords

all: chords

chords:
	(cd sm/hug-chords && git pull)
	$(MAKE) -C sm/hug-chords
	rsync -av --delete sm/hug-chords/pdfs .

upload:
	git add sm/hug-chords
	git add pdfs
	git commit -m "Commit for upload on `date`"
	git push
