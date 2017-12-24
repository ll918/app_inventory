#!/usr/bin/env python3
"""
Script that prints the inventory in a report format.

"""
import json

file = 'inventory.json'

with open(file) as f:
    inventory = json.load(f)

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
