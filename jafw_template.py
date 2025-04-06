import os
import re

VARIABLE_SUBSTITUTION = re.compile(r'\$([A-za-z_]+)|\$\{(.+?)\}')

def render_template(body, meta):
    template_file = get_template_file(meta.get('template', 'default'))
    return apply_data_to_templa_file(template_file, body, meta)

def get_template_file(fn):
    if type(fn) == list:
        fn = fn[0]

    with open(os.path.join('./system', 'template_' + fn + '.html')) as f:
        return f.read()


def apply_data_to_templa_file(template_file, body, meta):
    for var in re.finditer(VARIABLE_SUBSTITUTION, template_file):
        orig = var[0]
        varname = var[1] if var[1] is not None else var[2]
        template_file = template_file.replace(orig, load_var(varname, body, meta))

    return template_file


def load_var(varname, body, meta):
    if varname == 'Body':
        return body
    
    elif varname == 'Generator':
        return 'jafw'

    else:
        if varname in meta.keys():
            return meta[varname]
        
    return f'[not found: {varname}]'