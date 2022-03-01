import os


def get_folder_name(name):
    file_name, ext = os.path.splitext(name)
    return file_name + '_files'
