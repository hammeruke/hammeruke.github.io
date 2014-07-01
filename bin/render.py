#!/usr/bin/env python
import os
import sys
from jinja2 import Environment, FileSystemLoader

name = sys.argv[1]
tmpldir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'templates'))
env = Environment(loader=FileSystemLoader(tmpldir))
tmpl = env.get_template(name)
print tmpl.render()
