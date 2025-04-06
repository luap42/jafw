import os
import re
import datetime

VARIABLE_SUBSTITUTION = re.compile(r'\$([A-za-z_]+)|\$\{(.+?)\}')
PARTIAL_SUBSTITUTION = re.compile(r'\@partial\:([a-z]+)')
GALLERY_SUBSTITUTION = re.compile(r'\@gallery\:([a-z/]+)\{(.*?)?\}')

def render_template(body, meta):
    template_file = get_template_file(meta.get('template', 'default'))
    return apply_data_to_templa_file(template_file, body, meta)

def get_template_file(fn):
    if type(fn) == list:
        fn = fn[0]

    with open(os.path.join('./system', 'template_' + fn + '.html')) as f:
        return f.read()


def apply_data_to_templa_file(template_file, body, meta):
    while re.findall(PARTIAL_SUBSTITUTION, template_file):
        for partial in re.finditer(PARTIAL_SUBSTITUTION, template_file):
            orig = partial[0]
            partialname = partial[1]
            template_file = template_file.replace(orig, load_partial(partialname))

    for var in re.finditer(GALLERY_SUBSTITUTION, template_file):
        orig = var[0]
        subfolder = var[1]
        params = var[2]
        template_file = template_file.replace(orig, load_gallery(subfolder, params))

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



def load_gallery_files(params):
    with open(os.path.join('./system', 'gallery_' + params.get('list_tpl', 'list') + '.html')) as f:
        GALLERY_LIST = f.read()

    with open(os.path.join('./system', 'gallery_' + params.get('item_tpl', 'item') + '.html')) as f:
        GALLERY_ITEM = f.read()
    
    return GALLERY_LIST, GALLERY_ITEM


def load_gallery(subfolder, params):
    params = {(k := i.strip().split('='))[0] : (k[1] if len(k) == 2 else None) for i in params.split(',')}

    base_path = os.path.join(params.get('file_base', './assets/'), subfolder)

    GALLERY_LIST, GALLERY_ITEM = load_gallery_files(params)

    inner_html = []

    for elem in os.listdir(base_path):
        if (elem.startswith(".") and 'includedotfiles' not in params.keys()):
            continue

        target_path = f"{params.get('server_base', '/assets')}/{subfolder}/{elem}"

        elem_html = GALLERY_ITEM
        elem_html = elem_html.replace("$galleryItemName", os.path.splitext(elem)[0])
        elem_html = elem_html.replace("$galleryItemFileName", elem)
        elem_html = elem_html.replace("$galleryItem", target_path)

        inner_html.append(elem_html)

    return GALLERY_LIST.replace("$galleryContent", params.get('separator', '\n').replace('\\n', '\n').join(inner_html))
