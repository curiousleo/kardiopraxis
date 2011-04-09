from jinja2 import Template
from textile import textile
from sys import argv, exit
from ConfigParser import ConfigParser

def html_gen(page, title, template_path):
   input_path = page.lower() + '.textile',
   output_path = page.lower() + '.htm'}

   text = textile("".join(l for l in open(c['input_path'])))
   template = Template("".join(l for l in open(c['template_path'])))
   context = {'title': c['title'], 'content': text.decode('utf-8')}
   html = template.render(context).encode('utf-8')
   with open(c['output_path'], 'w') as output:
      output.write(html)
      print c['output_path'], "sucessfully written. Bye!"

if __name__ == "__main__":
   config = ConfigParser()
   config.read('site.cfg')
   template_path = config.get('template', 'path')
   for page, title in config.items('menu'):
      html_gen(page, title, templat_path)
