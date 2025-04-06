import os
from rcssmin import cssmin

def build_css():
    css_files = []

    css_files.append(load_css_file('./system/base.css'))

    for elem in os.listdir('./stylesheet/'):
        if elem == '.keep':
            continue

        css_files.append(load_css_file(os.path.join('./stylesheet/', elem)))

    css_file = '\n'.join(css_files)

    return cssmin(css_file)


def load_css_file(css_file):
    with open(css_file) as f:
        return f.read()