import os
import jafw_template
import shutil

def make_output(files, css):
    # write pages
    for file in files.items():
        make_single_file(*file)

    # write css
    with open('./build/style.css', 'w') as f:
        f.write(css)


def clear_build_folder():
    for elem in os.listdir("./build/"):
        if elem == ".keep":
            continue

        full_path = os.path.join("./build/", elem)

        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)


def copy_assets():
    shutil.copytree("./assets", "./build/assets")
    os.remove('./build/assets/.keep')


def make_single_file(fn, file):
    file_with_template = jafw_template.render_template(*file)
    full_fn = os.path.join('./build/', *os.path.split(fn)) + '.html'
    os.makedirs(os.path.split(full_fn)[0], exist_ok=True)

    with open(full_fn, 'w') as f:
        f.write(file_with_template)
