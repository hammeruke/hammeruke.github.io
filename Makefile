.PHONY: chords

all: chords

chords:
	$(MAKE) -C sm/hug-chords
	rsync -av --delete sm/hug-chords/pdfs .

upload:
	git add pdfs
	git commit -m "Commit for upload on `date`"
	git push
