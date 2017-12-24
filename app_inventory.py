#!/usr/bin/env python3
"""
On OSX, build an inventory of applications found in the Applications directory.

The inventory contains the name, path and version of the applications.  The
version data is obtained with the 'mdls' command.

The data gathered is save to json file.
"""
import json
import os
import subprocess

app_dir = '/Applications'
inventory = {}
file = 'inventory.json'


def build_inventory(app_path):
    # Build applications inventory dictionary.

    for item in os.scandir(app_path):
        if item.name.endswith('.app'):
            path = clean_path(item.path)
            try:
                version = os_command_str(
                    'mdls -name kMDItemVersion -raw ' + path)
                if version == '(null)':
                    version = 'n/a'
                inventory.update(
                    {item.name: {'path': path, 'version': version}})
            except Exception as e:
                print('There was a problem: %s' % e)
        else:
            if item.is_dir and not item.name.startswith('.'):
                new_path = os.path.join(app_path, item.name)
                if os.path.isdir(new_path):
                    build_inventory(new_path)


def clean_path(app_path):
    """ Add escape character('\') to file names.

    Spaces and other characters in path can cause problems when executing os
    command if not 'escaped'.
    """

    if ' ' in app_path:
        app_path = '\ '.join(app_path.split())
    if '(' in app_path:
        app_path = '\('.join(app_path.split('('))
    if ')' in app_path:
        app_path = '\)'.join(app_path.split(')'))
    return app_path


def os_command_str(command):
    # run an OS command (string) and return output as a string.

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output.decode()


build_inventory(app_dir)

if inventory:
    with open(file, 'w') as f:
        json.dump(inventory, f)
