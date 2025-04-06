import os
import re
import datetime

VARIABLE_SUBSTITUTION = re.compile(r'\$([A-za-z_]+)|\$\{(.+?)\}')
PARTIAL_SUBSTITUTION = re.compile(r'\@partial\:([a-z]+)')

def render_template(body, meta):
    template_file = get_template_file(meta.get('template', 'default'))
    return apply_data_to_templa_file(template_file, body, meta)

def get_template_file(fn):
    if type(fn) == list:
        fn = fn[0]

    with open(os.path.join('./system', 'template_' + fn + '.html')) as f:
        return f.read()


def apply_data_to_templa_file(template_file, body, meta):
    for partial in re.finditer(PARTIAL_SUBSTITUTION, template_file):
        orig = partial[0]
        partialname = partial[1]
        template_file = template_file.replace(orig, load_partial(partialname))

    for var in re.finditer(VARIABLE_SUBSTITUTION, template_file):
        orig = var[0]
        varname = var[1] if var[1] is not None else var[2]
        template_file = template_file.replace(orig, load_var(varname, body, meta))

    return template_file


def load_var(varname, body, meta):
    if varname == 'body':
        return body
    
    elif varname == 'generator':
        return 'jafw'
    
    elif varname == 'year':
        return str(datetime.datetime.now().year)

    else:
        if varname in meta.keys():
            return meta[varname][0]
        
    return f'[not found: {varname}]'



def load_partial(fn):
    with open(os.path.join('./system', 'partial_' + fn + '.html')) as f:
        return f.read()