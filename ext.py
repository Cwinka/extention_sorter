"""
    This scripts is aimed to sort files into any directory (not recursively)
    If the script does not know a defined file extention it'll show a proper message
    Feel free to add your extention or rename dirnames
"""
import os
import shutil
import sys


BASE_DIR = os.getcwd()
DIRECTORIES = {
    "HTML": ["html5", "html", "htm", "xhtml"],
    'CSS': ['css'],
    "IMAGES": ["jpeg", "jpg", "tiff", "gif", "bmp", "png", "bpg", "svg",
               "heif", "psd"],
    "VIDEOS": ["avi", "flv", "wmv", "mov", "mp4", "webm", "vob", "mng",
               "qt", "mpg", "mpeg", "3gp"],
    "DOCUMENTS": ["oxps", "epub", "pages", "docx", "doc", "fdf", "ods",
                  "odt", "pwi", "xsn", "xps", "dotx", "docm", "dox",
                  "rvg", "rtf", "rtfd", "wpd", "xls", "xlsx", "ppt",
                  "pptx"],
    "LINKS": ['lnk', "url"],
    'DATABASES': ['accdb'],
    'CORELDRAW': ['cdr'],
    'NORTON COMMANDER': ['rld'],
    "ARCHIVES": ["a", "ar", "cpio", "iso", "tar", "gz", "rz", "7z",
                 "dmg", "rar", "xar", "zip"],
    "AUDIO": ["aac", "aa", "aac", "dvf", "m4a", "m4b", "m4p", "mp3",
              "msv", "ogg", "oga", "raw", "vox", "wav", "wma"],
    "TEXT": ["txt", "in", "out", 'log'],
    "PDF": ["pdf"],
    'MySQL': ['msi'],
    "PYTHON": ["py", "pyw"],
    "XML": ["xml"],
    "EXE": ["exe"],
    "SHELL": ["sh"],
    "BAT": ['bat'],
    'DAT': ['dat'],
    "TORRENT": ["torrent"],
    "NOTEBOOK": ["gallerycollection"],
    "MetaQuotes": ["mq4", "mq5"],
    "CONTACTS": ["contact"],
    "BINARY": ["bin"],
    "ICONS": ["ico"],
    "CONFIG": ["ini"]

}
def turn_back(dirs: dict):
    """ Make a new dict with a structure:
        dict(
            list_1_elem_1: key_1, list_1_elem_2: key_1, list_1_elem_2: key_1,
            list_2_elem_1: key_2, list_2_elem_2: key_2
            etc..
        )
    """
    proper_dict = {}
    for key, values in dirs.items():
        for value in values:
            proper_dict[value.lower()] = key
    return proper_dict

files = [f for f in os.listdir('.') if os.path.isfile(f)]
removed_dirs = []
exceptions = set()
moved_files = []
proper_dict = turn_back(DIRECTORIES)

def get_ext(file):
    """ Return an extention of a given filepath """
    filename = os.path.split(file)[-1]
    ext = filename.split('.')[-1]
    return ext

def rm_empty_dir(dir_):
    try:
        os.rmdir(dir_)
    except:
        return
    removed_dirs.append(dir_)

def move_to(dir_, file):
    try:
        os.mkdir(dir_)
    except FileExistsError:
        pass
    shutil.move(os.path.join(BASE_DIR, file), os.path.join(BASE_DIR, dir_, file))

def move_back(file, directory):
    """ Moves all already moved files back to BASE_DIR directody
        (does't save positions)
    """
    shutil.move(os.path.join(BASE_DIR, directory, file), BASE_DIR)

def rollback(moved_files):
    print("Rollback")
    serv_dirs = {}
    for file in moved_files:
        ext = file.split('.')[-1]
        directory = proper_dict.get(ext)
        serv_dirs[directory] = 1
        move_back(file, directory)
    for key in serv_dirs:
        rm_empty_dir(key)

def show_info():
    print('\n')
    if removed_dirs:
        print(f"Removed dirs:\n")
        for dir in removed_dirs:
            print(f"\t{dir}")
        print('\n' + '-'*10 + '\n')
    if exceptions:
        print(f"These extentions are not determined:\n")
        for ext in exceptions:
            print(f"\t{ext}")
        print('\n' + '-'*10 + '\n')
    if moved_files:
        print("Moved files: ")
        for file in moved_files:
            print(f"\t{file}")
        print('\n' + '-'*10 + '\n')
    else:
        print("Nothing has been moved")

def group_file():
    for file in files:
        ext = get_ext(file)
        directory = proper_dict.get(ext)
        if directory is None:
            exceptions.add(ext)
            continue
        move_to(directory, file)
        moved_files.append(file)
    show_info()
    roll = input("Save it? (y/n): ")
    if roll.lower() != 'y':
        rollback(moved_files)

if __name__ == '__main__':
    group_file()
    del files
    del removed_dirs 
    del exceptions
    del moved_files 
    del proper_dict 