import os
import re

def extract_autosummary_methods(file, content):
    in_autosummary = False
    methods = []
    for line in content.splitlines():
        if 'autosummary' in line:
            in_autosummary = True
            continue
        if not line:
            # skip blank lines
            continue
        if not line.startswith(' '):
            in_autosummary = False
            continue
        method = line.lstrip()
        if in_autosummary and not method.startswith(':'):
            methods.append(method)
    return methods


dir = 'pandas-dev/doc/source/reference'
files = os.listdir(dir)
public_methods = []
for file in files:
    if file == 'index.rst':
        continue
    with open(os.path.join(dir, file)) as fd:
        content = fd.read()
    methods = extract_autosummary_methods(file, content)
    public_methods.extend(methods)

with open('public_methods.csv', 'w') as fd:
    fd.write('\n'.join(public_methods))

