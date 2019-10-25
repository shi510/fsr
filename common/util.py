import json
import importlib
import os
import csv

def open_config_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        file = json.load(f)
    return file

def remove_cr(line):
    if '\n' in line:
        return line.rpartition('\n')[0]
    return line

def read_lines_from_file(file, path_prefix, encoding):
    lines = []
    with open(file, 'r', encoding=encoding) as f:
        while True:
            line = f.readline()
            if line == '':
                break
            if '\n' in line:
                line = line.rpartition('\n')[0]
            lines.append(os.path.join(path_prefix, line))
    return lines

def write_file(name, x, y):
    with open(name, 'w') as f:
        for n in range(len(x)):
            for name in x[n]:
                f.write(str(x[n][name]))
                f.write(' ')
            f.write(str(y[n]))
            f.write('\n')
