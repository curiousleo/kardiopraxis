#!/usr/bin/python
# vim: expandtab tabstop=3 coding=utf8

from jinja2 import Template
from textile import textile
from sys import argv, exit
from ConfigParser import ConfigParser, NoSectionError, NoOptionError
from codecs import open as copen
from os import path as os_path, curdir

CONFIG = ConfigParser()

TEXTILE_DIR = HTML_DIR = SITE_PATH = curdir
CONF_PATH = 'site.cfg'
TEXTILE_EXT, HTML_EXT = 'textile', 'html'
TEMPLATE_PATH = 'template.' + HTML_EXT
NAVI = []

def html_gen(page, title=None):
   """Generates a html page using a jinja2 template and
   a textile-formatted content block."""
   if not title: title = page.title()
   input_path = _path(TEXTILE_DIR, page.lower() + '.' + TEXTILE_EXT)
   output_path = _path(HTML_DIR, page.lower() + '.' + HTML_EXT)

   text = textile(open(input_path).read())
   template = Template(open(TEMPLATE_PATH).read())
   context = {'title': title, 'content': text.decode('utf-8'), 
      'navigation': NAVI}
   html = template.render(context)

   with copen(output_path, encoding='latin-1', mode='w') as output:
      output.write(html)
      print 'Done:', page

def _path(a, *p):
   path = os_path.join(a, *p)
   if not os_path.isabs(path):
      path = os_path.abspath(os_path.join(SITE_PATH, path))
   return os_path.normpath(path)

def _cget(section, option, default=None):
   try:
      return CONFIG.get(section, option)
   except NoSectionError, NoOptionError:
      return default

def _help(exit_value = 0):
   print """Usage: %(prog)s [OPTION]... [CONFFILE [INPUTDIR OUTPUTDIR]]
Render html pages from a jinja2 template and textile content blocks.

   CONF        Path to configuration file.
   INPUTDIR    Directory of textile files.
   OUTPUTDIR   Directory of html files.

   -h --help   Show this help.

If no arguments are specified, %(prog)s looks for a file called '%(conf)s'
in the current directory.

If INPUTDIR and OUTPUTDIR are not given, %(prog)s tries to read them from
the configuration file.""" % {'prog': 'html_gen.py', 'conf': CONF_PATH}
   exit(exit_value)

if __name__ == '__main__':
   if '--help' in argv or '-h' in argv: _help()

   if len(argv) == 1:
      CONFIG.read(CONF_PATH)
      TEXTILE_DIR = _cget('input', 'dir', TEXTILE_DIR)
      HTML_DIR = _cget('output', 'dir', HTML_DIR)
   elif len(argv) == 2:
      CONFIG.read(argv[1])
      SITE_PATH = os_path.dirname(os_path.abspath(argv[1]))
      TEXTILE_DIR = _cget('input', 'dir', TEXTILE_DIR)
      HTML_DIR = _cget('output', 'dir', HTML_DIR)
   elif len(argv) == 4:
      CONFIG.read(argv[1])
      SITE_PATH = os_path.dirname(os_path.abspath(argv[1]))
      TEXTILE_DIR, HTML_DIR = argv[2], argv[3]
   else: _help(1)

   TEXTILE_EXT = _cget('input', 'ext', TEXTILE_EXT)
   HTML_EXT = _cget('output', 'ext', HTML_EXT)
   TEMPLATE_PATH = _path(_cget('template', 'path', TEMPLATE_PATH))
   NAVI = [{'url': page + HTML_EXT, 'title': title} \
      for page, title in CONFIG.items('navi')]

   print "Output dir:", _path(HTML_DIR)
   
   for page, title in CONFIG.items('navi'):
      try: html_gen(page, title)
      except IOError, e: print 'Error:', page, '\n', e
