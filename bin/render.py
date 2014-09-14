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

    args['folders'] = read_chords()
    args['pngs'] = read_pngs()

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

def relpath(root, fn):
    """Return a file name relative to root"""
    if not fn.startswith(root):
        raise ValueError("'%s' is not a prefix of '%s'" % (root, fn))
    return fn[len(root)+1:]

def read_chords():
    from collections import namedtuple
    Folder = namedtuple('Folder', 'title content')
    Pdf = namedtuple('Pdf', 'path title author')
    pdfroot = fullpath('pdfs')

    folders = []
    for (dirpath, dirnames, filenames) in os.walk(pdfroot):
        f = Folder(
            title=(relpath(pdfroot, dirpath) or 'books').title(),
            content=[])
        folders.append(f)
        for fn in filenames:
            if not fn.endswith('.pdf'):
                continue
            path = relpath(pdfroot, dirpath + '/' + fn)
            title, author = get_title_author(path)
            pdf = Pdf(
                path='pdfs/' + path,
                title=title, author=author)
            f.content.append(pdf)

        f.content.sort(key=attrgetter('title'))

    folders.sort(key=attrgetter('title'))

    return folders

def read_pngs():
    pngs = []
    for (dirpath, dirnames, filenames) in os.walk('pngs'):
        for fn in filenames:
            if fn.endswith('.png'):
                path = dirpath + '/' + fn
                pngs.append(path)

    pngs.sort()
    return pngs

if __name__ == '__main__':
    import sys
    name = sys.argv[1]
    print render(name)
