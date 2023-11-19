#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path
from typing import Union
from shutil import which
from sys import platform
from xml.etree import ElementTree
from os import path
from subprocess import check_output, run
from subprocess import CalledProcessError


def parse(recent_projects_file):
    root = ElementTree.parse(recent_projects_file).getroot()
    entries = root.findall(".//component[@name='RecentProjectsManager']//entry[@key]")

    projects = []
    for entry in entries:
        project_path = entry.attrib["key"].replace("$USER_HOME$", str(Path.home()))

        tag_opened = entry.find(".//option[@name='projectOpenTimestamp']")
        last_opened = tag_opened.attrib["value"] if tag_opened is not None and "value" in tag_opened.attrib else None

        if project_path and last_opened:
            projects.append( (Path(project_path).name, project_path, last_opened))
    return sorted(projects, key=lambda p: p[2], reverse=True)


def run_rofi(projects):
    browser = "idea.sh"
    options = "\n".join([f"{p[0]}\t{p[1]}" for p in projects])
    try:
        selection = check_output(['rofi', '-i', '-dmenu'],
                                 input=options.encode()
                                 ).decode().strip()
        url = selection.split('\t')[1]
        run([browser, url])
    except CalledProcessError as e:
        pass




if __name__ == '__main__':
    projects = parse(path.expanduser("~")+"/.config/JetBrains/recentProjects.xml")
    run_rofi(projects)

