import os

def render_template(body, meta):
    template_file = get_template_file(meta.get('template', 'default'))
    return apply_data_to_templa_file(template_file, body, meta)

def get_template_file(fn):
    if type(fn) == list:
        fn = fn[0]

    with open(os.path.join('./system', 'template_' + fn + '.html')) as f:
        return f.read()


def apply_data_to_templa_file(template_file, body, meta):
    return template_file