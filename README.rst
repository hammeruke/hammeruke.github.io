Hammersmith Ukulele Group website
=================================

Rendered on http://hammeruke.github.io/ and http://hug.spacehobo.com/

Check out the project with:

    git clone --recursive git@github.com:hammeruke/hammeruke.github.io.git

This will initialize the submodules: the hug-songs, contains the chords, and
hug-songs' own submodules, which are fonts used for rendering.

After checking out please run::

    cd hammeruke.github.io
    make touch

This will mark the generated files as up-to-date and avoid that a run of
`make` will change all the site content.

To start working on the project::

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt

To update the website (e.g. changing the html)::

    [change the pages]
    make
    make upload

Changes to the chords should be made instead in the `hug-chords repository`__
To include the new songs and changes that have been committed to the
`hug-chords` repos you can run::

    make newsongs
    make upload

.. __: https://github.com/hammeruke/hug-chords
