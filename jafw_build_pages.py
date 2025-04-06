import os
import re
import markdown

def build_pages(path="./pages/", prefix=None):
    pages = {}
    for elem in os.listdir(path):
        if elem == ".keep":
            continue

        elem_name = make_element_name(elem, prefix)
        full_path = os.path.join(path, elem)

        if os.path.isdir(full_path):
            pages.update(build_pages(full_path, prefix=elem_name))
        else:
            pages[elem_name] = build_single_page(full_path)

    return pages


def make_element_name(elem, prefix):
    fn = os.path.splitext(elem)[0]
    fn = fn.replace("_", "-")
    fn = re.sub('[^a-zA-Z0-9-]', '-', fn)
    fn = re.sub('-+', '-', fn)

    if prefix is not None:
        fn = prefix + "/" + fn

    return fn

def build_single_page(full_path):
    with open(full_path) as r:
        md = r.read()
    
    mdobj = markdown.Markdown(extensions=['meta', 'extra'])
    html = mdobj.convert(md)
    return html, mdobj.Meta