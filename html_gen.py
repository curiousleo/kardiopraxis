from jinja2 import Template
from textile import textile
from sys import argv, exit

def html_gen(c):
   text = textile("".join(l for l in open(c['input_path'])))
   template = Template("".join(l for l in open(c['template_path'])))
   context = {'title': c['title'], 'content': text.decode('utf-8')}
   html = template.render(context).encode('utf-8')
   with open(c['output_path'], 'w') as output:
      output.write(html)
      print c['output_path'], "sucessfully written. Bye!"

if __name__ == "__main__":
   if len(argv) != 3:
      print "Wrong # of arguments!"; exit()

   gen_context = {
      'title': argv[1],
      'template_path': argv[2],
      'input_path': argv[1].lower() + '.textile',
      'output_path': argv[1].lower() + '.htm'}
   html_gen(gen_context)
