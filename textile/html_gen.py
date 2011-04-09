# vim: expantab tabstop=3 coding=utf8

from jinja2 import Template
from textile import textile
from sys import argv, exit
from ConfigParser import ConfigParser
from codecs import open as copen
from os import path as os_path, curdir

TEXTILE_PATH = HTML_PATH = curdir
TEXTILE_EXT, HTML_EXT = 'textile', 'html'
TEMPLATE_PATH = 'template.' + HTML_EXT
NAVI = []

def html_gen(page, title=None):
   if not title: title = page.title()
   input_path = os_path.join(TEXTILE_PATH, page.lower() + TEXTILE_EXT)
   output_path = os_path.join(HTML_PATH, page.lower() + HTML_EXT)

   text = textile(open(input_path).read())
   template = Template(open(TEMPLATE_PATH).read())
   context = {'title': title, 'content': text.decode('utf-8'), 
      'navigation': NAVI}
   html = template.render(context)

   with copen(output_path, encoding='latin-1', mode='w') as output:
      output.write(html)
      print output_path, 'done.'

if __name__ == '__main__':
   config = ConfigParser()
   config.read('site.cfg')

   if len(argv) == 1:
      TEXTILE_PATH = config.get('input', 'dir')
      HTML_PATH = config.get('output', 'dir')
   elif len(argv) == 3: TEXTILE_PATH, HTML_PATH = argv[1], argv[2]
   else: exit(-1)

   TEXTILE_EXT = config.get('input', 'ext')
   HTML_EXT = config.get('output', 'ext')
   TEMPLATE_PATH = config.get('template', 'path')
   NAVI = [{'url': page + HTML_EXT, 'title': title} \
      for page, title in config.items('navi')]

   for page, title in config.items('navi'):
      try: html_gen(page, title)
      except IOError, e: print e
