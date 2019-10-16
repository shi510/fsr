import argparse
import math
import os
import numpy as np
import common.util as cutil
import preprocessing.util as putil
import preprocessing.statistic as statistic
import preprocessing.convert as convert

parser = argparse.ArgumentParser()
parser.add_argument('--config_file')
parser.add_argument('--print_statistics', type=bool)

if __name__ == '__main__':
    args = parser.parse_args()
    cfg = cutil.open_config_file(args.config_file)

    if args.print_statistics:
        for file in cfg['files']:
            print('File: {}'.format(file))
            dict_list = cutil.convert_csv2dict_list(file, cfg['interestings'])
            statistic.print_statistics(dict_list)
    else:
        for file in cfg['files']:
            dict_list = cutil.convert_csv2dict_list(file, cfg['interestings'])
            dict_list = statistic.normalize(dict_list, convert.norm_lambdas)
            x, y = cutil.make_past_pair(dict_list, cfg['past_hour'], convert.past_pair)
            file_name = os.path.basename(file)
            cutil.write_file('preprocessed_' + file_name, x, y)
