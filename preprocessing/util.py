import importlib
import os
import csv
import common.util as cutil

def load_cvt(model_type):
    as_file = model_type.rpartition('.')[0]
    as_fn = model_type.rpartition('.')[2]
    return getattr(importlib.import_module(as_file), as_fn)

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

"""
convert meteorological data csv file into the format as below:

{
    attribute_name: attribute_value,
    ...
}

"""
def convert_csv2dict_list(csv_list, interestings):
    dict_list = []
    root_path = os.path.dirname(csv_list)
    files = read_lines_from_file(csv_list, root_path, 'utf-8')
    
    cvt_fns = {
        it_name: load_cvt(interestings[it_name]) for it_name in interestings
    }

    for file in files:
        f = open(file, 'r', encoding='euc-kr')
        title = cutil.remove_cr(f.readline()).split(',')
        while True:
            vals = cutil.remove_cr(f.readline()).split(',')
            if len(vals) == 1:
                break
            attrs = {}
            for it in interestings:
                try:
                    idx = title.index(it)
                except:
                    raise 'Not found ' + it
                cvt_dict = cvt_fns[it](vals[idx])
                for dict_name in cvt_dict:
                    attrs[dict_name] = cvt_dict[dict_name]
            dict_list.append(attrs)
        f.close()
    return dict_list

def make_past_pair(dict_list, past_hour, past_pair):
    x = []
    y = []
    input_list = past_pair['input']
    output = past_pair['output']
    for n in range(past_hour, len(dict_list)):
        pair = {}
        
        for name in input_list:
            pair[name] = dict_list[n][name]
            if input_list[name] == True:
                for p in range(1, past_hour+1):
                    pair[name+str(-p)] = dict_list[n-p][name]
        
        x.append(pair)
        y.append(dict_list[n][output])
    return x, y

def write_file(name, x, y):
    with open(name, 'w') as f:
        for n in range(len(x)):
            for name in x[n]:
                f.write(str(x[n][name]))
                f.write(' ')
            f.write(str(y[n]))
            f.write('\n')
