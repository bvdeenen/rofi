#!/usr/bin/env python

from os import path
import json
import jq
from os import path
from subprocess import check_output, run, STDOUT
from subprocess import CalledProcessError
from sys import argv

def main():
    browser = "google-chrome"
    pairs = parse_chrome()
    options = "\n".join(["\t".join(a) for a in pairs])

    try:
        theme= path.expanduser("~") +"/.config/rofi/launchers/type-5/style-1.rasi"
        selection = check_output(['rofi', '-i', '-dmenu', '-theme', theme],
                                 input=options.encode()
                                 ).decode().strip()
        url = selection.split('\t')[1]
        run([browser, url])
    except CalledProcessError as e:
        pass

def parse_chrome(file_path=None):
    if file_path is None:
        bookmarks_path = path.expanduser("~") + "/.config/google-chrome/Default/Bookmarks"
    else:
        bookmarks_path = path.expanduser(file_path)

    if not path.isfile(bookmarks_path):
        print("No bookmarks file found!")
        exit()

    with open(bookmarks_path, "r") as _f:
        bookmarks = json.load(_f)
    return jq.compile('..|select(.type?=="url")|[.name,.url]').input_value(bookmarks)


if __name__ == "__main__":
    main()

