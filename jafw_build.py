import argparse

import jafw_build_pages
import jafw_css_compressor
import jafw_minifer

parser = argparse.ArgumentParser(
    prog='jafw',
    description='just another f-ing website-generator'
)

args = parser.parse_args()

files = jafw_build_pages.build_pages()
files = jafw_build_pages.resolve_links(files)
css = jafw_css_compressor.build_css()

output = jafw_minifer.make_output()