#
# Copyright (c) Simon Zuend
#

import json
import os
from shutil import copytree, rmtree, ignore_patterns, make_archive

# Reads info.json to create the package name
def package_name():
    with open('info.json') as info_file:
        info = json.load(info_file)
        return info['name'] + "_" + info['version']
    raise Exception("Unable to read info.json!")

def zipdir(path, handle):
    for root, dirs, files in os.walk(path):
        for file in files:
            handle.write(file)

def main():
    package = package_name()
    out_directory = os.path.join(os.getcwd(), 'out')
    
    if os.path.exists(out_directory):
       rmtree(out_directory)

    # Create 'out' directory
    os.mkdir(out_directory)

    # Copy all files except build results and git stuff.
    target_directory = os.path.join(out_directory, package)
    copytree(os.getcwd(), target_directory,
        ignore=ignore_patterns('package-mod.py', 'out', '.git', '.gitignore', '*.zip'))
    
    # Delete any old packages with the same name if they exist.
    file_name = package + '.zip'
    if os.path.exists(file_name):
        os.remove(file_name)

    # Zip up the contents
    # zipf = zipfile.ZipFile(file_name, 'w', zipfile.ZIP_DEFLATED)
    # zipdir(out_directory, zipf)
    # zipf.close()
    make_archive(package, "zip", root_dir=out_directory)

    # Delete the output directory
    rmtree(out_directory)

if __name__ == "__main__":
    main()
