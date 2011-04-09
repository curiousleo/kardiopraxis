# vim: expantab tabstop=3 coding=utf8

from jinja2 import Template
from textile import textile
from sys import argv, exit
from ConfigParser import ConfigParser
from codecs import open as copen
from os import path as os_path, curdir

TEXTILE_PATH = HTML_PATH = curdir

def html_gen(page, title=None, navi=[], template_path='template.htm'):
   if not title: title = page.title()
   input_path = os_path.join(TEXTILE_PATH, page.lower() + '.textile')
   output_path = os_path.join(HTML_PATH, page.lower() + '.htm')

   text = textile(open(input_path).read())
   template = Template(open(template_path).read())
   context = {'title': title, 'content': text.decode('utf-8'), 
      'navigation': navi}
   html = template.render(context)

   with copen(output_path, encoding='latin-1', mode='w') as output:
      output.write(html)
      print output_path, "sucessfully written."

if __name__ == "__main__":
   if   len(argv) == 1: pass
   elif len(argv) == 2: TEXTILE_PATH = HTML_PATH = argv[1]
   elif len(argv) == 3: TEXTILE_PATH, HTML_PATH = argv[1], argv[2]
   else: exit(-1)

   config = ConfigParser()
   config.read('site.cfg')

   template_path = config.get('template', 'path')
   navi = [{'url': page + '.htm', 'title': title} \
      for page, title in config.items('menu')]

   for page, title in config.items('menu'):
      try: html_gen(page, title, navi, template_path)
      except IOError, e: print e
