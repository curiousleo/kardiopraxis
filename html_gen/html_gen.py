#!/usr/bin/python
# vi: expandtab tabstop=3 coding=utf8

from jinja2 import Template
from textile import textile
from sys import argv, exit
from ConfigParser import ConfigParser, NoSectionError, NoOptionError
from codecs import open as copen
from os import path as os_path, curdir

CONFIG = ConfigParser()

SITE_PATH = curdir
CONF_PATH = 'site.cfg'
NAVI = []

HELP_TEXT = '''Usage: %(prog)s [OPTION]... [CONFFILE [INPUTDIR OUTPUTDIR]]
Render html pages from a jinja2 template and textile content blocks.

   CONF        Path to configuration file.
   INPUTDIR    Directory of textile files.
   OUTPUTDIR   Directory of html files.

   -h --help   Show this help.

If no arguments are specified, %(prog)s looks for a file called '%(conf)s'
in the current directory.

If INPUTDIR and OUTPUTDIR are not given, %(prog)s tries to read them from
the configuration file.''' % {'prog': 'html_gen.py', 'conf': CONF_PATH}

DEFAULT_CONF = '''[navi]
index = Homepage
[paths]
template = template.html
output_dir = .
output_ext = html
input_dir = .
input_ext = textile
site_dir = .'''

def html_gen(page, title=None):
   '''Generates a html page using a jinja2 template and
   a textile-formatted content block.'''
   if not title: title = page.title()

   input_path = _path(_cget('paths', 'input_dir'), 
      page.lower() + '.' + _cget('paths', 'input_ext'))
   output_path = _path(_cget('paths', 'output_dir'),
      page.lower() + '.' + _cget('paths', 'output_ext'))

   content = textile(open(input_path).read())
   template = Template(open(_path(_cget('paths', 'template'))).read())
   context = {'title': title, 'content': content.decode('utf-8'), 
      'navigation': NAVI}
   html = template.render(context)

   with copen(output_path, encoding='latin-1', mode='w') as output:
      output.write(html)

def _path(p1, p2=''):
   '''Takes one or two paths. Returns an absolute norm path.'''
   if os_path.isabs(p2): return os_path.normpath(p2)
   path = os_path.normpath(os_path.join(p1, p2))
   if not os_path.isabs(path):
      path = os_path.abspath(os_path.join(SITE_PATH, path))
   return path

def _cget(section, option):
   '''Shorthand for CONFIG.get(...).'''
   return CONFIG.get(section, option)

def _cset(section, option, value):
   '''Shorthand for CONFIG.set(...).'''
   CONFIG.set(section, option, value)

def _help(exit_value = 0):
   '''Prints help message and exits the programme.'''
   print HELP_TEXT
   exit(exit_value)

class DefaultConfig(object):
   '''Provides a file-like object for the default configuration that can be
read by ConfigParser, i.e. ConfigParser.readfp(DefaultConfig()).'''
   def __init__(self):
      '''Initialises the '_lines' generator'''
      self._lines = (l + '\n' for l in DEFAULT_CONF.split('\n'))
   def readline(self):
      '''Emulates file readline behaviour'''
      try: return self._lines.next()
      except StopIteration: return ''

if __name__ == '__main__':
   if '--help' in argv or '-h' in argv: _help()

   # Set up defaults
   CONFIG.readfp(DefaultConfig())
   conf_path = CONF_PATH

   if len(argv) == 1:
      CONFIG.read(CONF_PATH)
   elif len(argv) == 2:
      # Config file given
      conf_path = os_path.abspath(argv[1])
      CONFIG.read(conf_path)
      _cset('paths', 'site_dir', os_path.dirname(conf_path))
   elif len(argv) == 4:
      # Config file, input dir and output dir given
      conf_path = os_path.abspath(argv[1])
      CONFIG.read(conf_path)
      _cset('paths', 'site_dir', os_path.dirname(conf_path))
      _cset('paths', 'input_dir', argv[2])
      _cset('paths', 'output_dir', argv[3])
   else: _help(1)

   NAVI = [{'url': page + _cget('paths', 'output_ext'),
      'title': title} for page, title in CONFIG.items('navi')]

   site_dir = _path(_cget('paths', 'site_dir'))
   input_dir = _path(site_dir, _cget('paths', 'input_dir'))
   output_dir = _path(site_dir, _cget('paths', 'output_dir'))
   template_path = _path(site_dir, _cget('paths', 'template'))

   _cset('paths', 'input_dir', input_dir)
   _cset('paths', 'output_dir', output_dir)
   _cset('paths', 'template', template_path)

   _rel = lambda p: os_path.relpath(p)
   print 'Conf file :', _rel(conf_path)
   print 'Input dir :', _rel(input_dir)
   print 'Output dir:', _rel(output_dir)
   print 'Template  :', _rel(template_path)
   
   for page, title in CONFIG.items('navi'):
      print 'Converting', page, '...',
      try: html_gen(page, title); print 'done.'
      except IOError, e: print '\n', 'Error:', page, '\n', e
