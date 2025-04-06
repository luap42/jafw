import os
import shutil

def make_output(files, css):
    return ""


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
    pass