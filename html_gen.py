from jinja2 import Template
from textile import textile
from sys import argv, exit
from ConfigParser import ConfigParser
import codecs

def html_gen(page, title=None, navi=[], template_path='template.htm'):
   if not title: title = page.title()
   input_path = page.lower() + '.textile'
   output_path = page.lower() + '.htm'

   text = textile(open(input_path).read())
   template = Template(open(template_path).read())
   context = {'title': title, 'content': text.decode('utf-8'), 'navigation': navi}
   html = template.render(context)

   with codecs.open(output_path, encoding='latin-1', mode='w') as output:
      output.write(html)
      print output_path, "sucessfully written."

if __name__ == "__main__":
   config = ConfigParser()
   config.read('site.cfg')

   template_path = config.get('template', 'path')
   navi = [{'url': page + '.htm', 'title': title} \
      for page, title in config.items('menu')]

   for page, title in config.items('menu'):
      try: html_gen(page, title, navi, template_path)
      except IOError, e: print e
