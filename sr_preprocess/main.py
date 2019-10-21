import argparse
import math
import os
import numpy as np
import common.util as cutil
import sr_preprocess.statistic as statistic
import sr_preprocess.convert as convert
import tensorflow as tf

parser = argparse.ArgumentParser()
parser.add_argument('tfrecord')
parser.add_argument('-cfg')
parser.add_argument('--print_statistics', type=bool)

def _tf_float_list(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

def make_tfrecord(file, interestings, future_hour, past_hour, past_pair):
    dict_list = cutil.convert_csv2dict_list(file, interestings)
    dict_list = statistic.normalize(dict_list, convert.norm_lambdas)
    x, y = cutil.make_past_pair(
        dict_list, future_hour, past_hour, past_pair)
    file_name = os.path.splitext(os.path.basename(file))[0]
    tf_file = tf.io.TFRecordWriter(file_name+'.tfrecord')
    for a, b in zip(x, y):
        features = []
        for name in a:
            features.append(a[name])
        feature = {
            'features': _tf_float_list(features),
            'radiation': _tf_float_list([b])
        }
        exam = tf.train.Example(features=tf.train.Features(feature=feature))
        tf_file.write(exam.SerializeToString())
    tf_file.close()

if __name__ == '__main__':
    args = parser.parse_args()

    if args.tfrecord:
        cfg = cutil.open_config_file(args.cfg)
        for file in cfg['files']:
            make_tfrecord(file, cfg['interestings'], cfg['future_hour'], cfg['past_hour'], convert.past_pair)
    if args.print_statistics:
        for file in cfg['files']:
            print('File: {}'.format(file))
            dict_list = cutil.convert_csv2dict_list(file, cfg['interestings'])
            statistic.print_statistics(dict_list)
