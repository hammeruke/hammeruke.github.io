#!/usr/bin/env python

import re
import os
from operator import attrgetter
from jinja2 import Environment, FileSystemLoader

def fullpath(*components):
    """Return a path in the project tree"""
    return os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', *components))

tmpldir = os.path.abspath(os.path.join('templates'))
env = Environment(loader=FileSystemLoader(tmpldir))

def render(name):
    tmpl = env.get_template(name)
    args = {}

    args['folders'], args['pngs'] = read_chords()

    return tmpl.render(**args)

def get_title_author(path):
    title = author = None
    cho = fullpath('hug-chords', 'chords', os.path.splitext(path)[0] + '.cho')
    if os.path.isfile(cho):
        rex = re.compile(r'^\s*{(t|st):([^}]+)}\s*$')
        for line in open(cho):
            m = rex.match(line)
            if m is None: continue
            if m.group(1) == 't':
                title = m.group(2)
            elif m.group(1) == 'st':
                author = m.group(2)
            if title is not None and author is not None:
                break

    if not title:
        title = os.path.splitext(os.path.split(path)[-1])[0].title() \
                .replace('-', ' ')

    return title, author

def read_chords():
    from collections import namedtuple
    Folder = namedtuple('Folder', 'title content')
    Pdf = namedtuple('Pdf', 'path title author')
    Png = namedtuple('Png', 'path')
    pdfroot = fullpath('hug-chords', 'pdfs')

    def relpath(fn):
        """Return a file name relative to pdfroot"""
        return fn[len(pdfroot)+1:]

    folders = []
    pngs = []
    for (dirpath, dirnames, filenames) in os.walk(pdfroot):
        f = Folder(
            title=(relpath(dirpath) or 'books').title(),
            content=[])
        folders.append(f)
        for fn in filenames:
            if fn.endswith('.png'):
                path = relpath(dirpath + '/' + fn)
                pngs.append(Png(path))
            if not fn.endswith('.pdf'):
                continue
            path = relpath(dirpath + '/' + fn)
            title, author = get_title_author(path)
            pdf = Pdf(
                path='pdfs/' + path,
                title=title, author=author)
            f.content.append(pdf)

        f.content.sort(key=attrgetter('title'))

    folders.sort(key=attrgetter('title'))

    return folders, pngs

if __name__ == '__main__':
    import sys
    name = sys.argv[1]
    print render(name)
