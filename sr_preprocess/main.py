import argparse
import math
import os
import numpy as np
import common.util as cutil
import sr_preprocess.statistic as statistic
import sr_preprocess.convert as convert
import tensorflow as tf
from common.registry import Registry

parser = argparse.ArgumentParser()
parser.add_argument('tfrecord')
parser.add_argument('-cfg')
parser.add_argument('--print_statistics', type=bool)

def _tf_float_list(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

def make_tfrecord(file, past_hour, future_hour):
    x, y = convert.make_dataset(file, past_hour, future_hour, 5, 21)
    file_name = os.path.splitext(os.path.basename(file))[0]
    tf_file = tf.io.TFRecordWriter(file_name+'.tfrecord')
    for a, b in zip(x, y):
        feature = {
            'features': _tf_float_list(a),
            'radiation': _tf_float_list(b)
        }
        exam = tf.train.Example(features=tf.train.Features(feature=feature))
        tf_file.write(exam.SerializeToString())
    tf_file.close()

if __name__ == '__main__':
    args = parser.parse_args()

    if args.tfrecord:
        cfg = cutil.open_config_file(args.cfg)
        for file in cfg['files']:
            make_tfrecord(file, cfg['past_hour'], cfg['future_hour'])
        print("input size:", convert.size_of_input_transform(cfg["past_hour"]))
    if args.print_statistics:
        for file in cfg['files']:
            print('File: {}'.format(file))
            dict_list = cutil.convert_csv2dict_list(file, cfg['interestings'])
            statistic.print_statistics(dict_list)
