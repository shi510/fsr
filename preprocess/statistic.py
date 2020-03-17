import os
from common.registry import Registry
import common.util as cutil
import common.io_register as io_register
import numpy as np
import sys

def get_statistic(csv_list):
    root_path = os.path.dirname(csv_list)
    files = cutil.read_lines_from_file(csv_list, root_path, 'utf-8')
    min_max_table = {}
    for key in Registry.REGISTRY_LIST:
        if Registry.REGISTRY_LIST[key]['statistic']:
            min_max_table[key] = {
                "min": sys.float_info.max,
                "max": sys.float_info.min
            }
    for file in files:
        f = open(file, 'r', encoding='euc-kr')
        title = cutil.remove_cr(f.readline()).split(',')
        while True:
            vals = cutil.remove_cr(f.readline()).split(',')
            if len(vals) == 1:
                break
            for key in min_max_table:
                try:
                    idx = title.index(key)
                except:
                    raise 'Not found ' + key
                val = float(vals[idx]) if vals[idx] != '' else 0.
                if min_max_table[key]["min"] > val:
                    min_max_table[key]["min"] = val
                if min_max_table[key]["max"] < val:
                    min_max_table[key]["max"] = val
        f.close()
    return min_max_table
