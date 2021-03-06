#!/usr/bin/env python3
"""
On OSX, build an inventory of applications found in the Applications directory.

The inventory contains the name, path and version of the applications.

The data gathered is saved to json file.

https://docs.python.org/3/library/plistlib.html
https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man5/plist.5.html
"""
import json
import os
import plistlib

file = 'inventory.json'


def build_inventory(app_path='/Applications'):
    # Build applications inventory dictionary.

    inventory = {}
    for item in os.scandir(app_path):
        if item.name.endswith('.app'):
            path = item.path
            try:
                with open(os.path.join(path, 'Contents/Info.plist'),
                          'rb') as f:
                    properties = plistlib.load(f)
                version = properties.get('CFBundleShortVersionString', 'n/a')

                inventory.update(
                    {item.name: {'path': path, 'version': version}})
            except Exception as e:
                print('There was a problem: %s' % e)
        else:
            if item.is_dir and not item.name.startswith('.'):
                new_path = os.path.join(app_path, item.name)
                if os.path.isdir(new_path):
                    build_inventory(new_path)
    if inventory:
        with open(file, 'w') as f:
            json.dump(inventory, f)
    return inventory


inventory = build_inventory()

app_lst = []
for k, v in inventory.items():
    entry = ' '.join([k, v['version']])
    app_lst.append(entry)
app_lst.sort(key=str.lower)

print('Applications inventory')
print()
for i in app_lst:
    print(i)
print()
print(len(inventory), 'applications installed.')
