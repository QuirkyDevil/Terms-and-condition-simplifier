# check for empty files in backend directory and delete them

import os
import shutil


def test_empty_files():
    for root, _, files in os.walk("backend"):
        for file in files:
            if os.stat(os.path.join(root, file)).st_size == 0:
                print("Empty file: " + os.path.join(root, file))
                os.remove(os.path.join(root, file))


def test_empty_folders():
    for root, dirs, _ in os.walk("backend"):
        for directory in dirs:
            if not os.listdir(os.path.join(root, directory)):
                shutil.rmtree(os.path.join(root, directory))
