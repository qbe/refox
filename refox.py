#!/usr/bin/env python3

# refox.py - firefox window repositioner for sway
#
# Written in 2025 by Lukas "qbe" Hannen
#
# To the extent possible under law,
# the author(s) have dedicated all copyright
# and related and neighboring rights to this software
# to the public domain worldwide.
# This software is distributed without any warranty.
#
# You should have received a copy of the
# CC0 Public Domain Dedication along with this software.
# If not, see <http://creativecommons.org/publicdomain/zero/1.0/>. 

import subprocess
import json

from re import escape

def walk(tree, current_workspace=None):
    workspace = current_workspace
    match tree["type"]:
        case "con":
            if "app_id" in tree:
                if tree["app_id"] == "firefox":
                    return [(workspace, tree["name"])]
        case "workspace":
            workspace = tree["name"]

    return sum([walk(n, current_workspace=workspace) for n in tree["nodes"]], start=[])

def reposition(fox):
    workspace, title = fox
    title = escape(title).replace('"', '\\"')
    try:
        cmd = [
                'swaymsg',
                '-r',
                f'[title="{title}"]',
                'move',
                'window',
                'to',
                'workspace',
                f'{workspace}'
            ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exp:
        print(f'window titled "{title}" could not be moved to workspace "{workspace}": {exp.stderr}')
        pass

def main():
    cmd = ["swaymsg", "-r", "-t", "get_tree"]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
    tree = json.loads(proc.stdout)
    foxes = walk(tree)
#    print(json.dumps(foxes, indent=4))
    print("saved firefox window positions")
    input("restart firefox, then press Enter...")
    for fox in foxes:
        reposition(fox)

if __name__ == '__main__':
    main()
