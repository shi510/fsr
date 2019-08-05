import json

def open_config_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        file = json.load(f)
    return file

def remove_cr(line):
    if '\n' in line:
        return line.rpartition('\n')[0]
    return line