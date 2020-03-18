import argparse
import math
import os
import numpy as np
import common.util as cutil
import preprocess.statistic as statistic
import preprocess.convert as convert
import tensorflow as tf
from common.registry import Registry

parser = argparse.ArgumentParser()

sub_parser = parser.add_subparsers(dest='cmd')
tfrecord_parser = sub_parser.add_parser('tfrecord')
tfrecord_parser.add_argument('-cfg')

statistic_parser = sub_parser.add_parser('show_statistic')
statistic_parser.add_argument('-cfg')

def _tf_float_list(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

def _tf_int64_list(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=value))

def make_tfrecord(file, past_hour, future_hour):
    dataset = convert.make_dataset(file, past_hour, future_hour, 5, 21)
    file_name = os.path.splitext(os.path.basename(file))[0]
    tf_file = tf.io.TFRecordWriter(file_name+'.tfrecord')
    for data in dataset:
        feature = {
            "date": _tf_int64_list(data["date"]),
            'features': _tf_float_list(data["features"]),
            'radiation': _tf_float_list(data["radiation"])
        }
        exam = tf.train.Example(features=tf.train.Features(feature=feature))
        tf_file.write(exam.SerializeToString())
    tf_file.close()

if __name__ == '__main__':
    args = parser.parse_args()

    if args.cmd == 'tfrecord':
        cfg = cutil.open_config_file(args.cfg)
        for file in cfg['files']:
            make_tfrecord(file, cfg['past_hour'], cfg['future_hour'])
        print("input size:", convert.size_of_input_transform(cfg["past_hour"]))
    if args.cmd == 'show_statistic':
        cfg = cutil.open_config_file(args.cfg)
        for file in cfg['files']:
            print('File: {}'.format(file))
            stat = statistic.get_statistic(file)
            print(stat)
