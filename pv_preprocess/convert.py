import os
import tensorflow as tf
from common.registry import Registry
import common.util as cutil
import common.io_register as io_register
import numpy as np

def norm(val, min, max):
    return (val - min) / (max - min)

@io_register.regist_output("pvgen", future=True)
class CvtDate:
    min = 1
    max = 12

    @classmethod
    def transform(cls, pvgen):
        gen = norm(float(pvgen), cls.min, cls.max)
        gen = float(pvgen)
        return gen

    @staticmethod
    def size():
        return 1


def _parse(proto):
    feature_disc = {
        "date": tf.io.FixedLenFeature([], tf.int64),
        'features': tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
        'radiation': tf.io.FixedLenFeature([], tf.float32)
    }
    exam = tf.io.parse_single_example(proto, feature_disc)
    return (exam["date"], exam['features'], exam['radiation'])


def _make_day_indexed_table_for_pvgen(csv_list):
    root_path = os.path.dirname(csv_list)
    files = cutil.read_lines_from_file(csv_list, root_path, 'utf-8')
    table = {}
    for file in files:
        f = open(file, 'r', encoding='euc-kr')
        title = cutil.remove_cr(f.readline()).split(',')
        while True:
            vals = cutil.remove_cr(f.readline()).split(',')
            if len(vals) == 1:
                break
            try:
                idx_date = title.index("date")
                idx_tm = title.index("tm")
            except:
                raise 'Not found ' + "일시"
            day = int(vals[idx_date] + vals[idx_tm])
            attrs = {}
            for key in Registry.REGISTRY_LIST:
                fn = Registry.REGISTRY_LIST[key]["fn"]
                try:
                    idx = title.index(key)
                except:
                    raise 'Not found ' + key
                attrs[key] = {
                    "value": fn.transform(vals[idx])
                }
            table[day] = attrs
        f.close()
    return table


def _make_day_indexed_table_for_tfrecord(ds):
    table = {}
    for ds_data in ds:
        date = ds_data[0].numpy()
        features = ds_data[1].numpy()
        table[date] = features
    return table

def make_dataset(sr_tfrecord, pv_file, sr_model, future_hour):
    dataset=[]
    ds = tf.data.TFRecordDataset(sr_tfrecord)
    ds = ds.map(_parse)
    pvgen_table = _make_day_indexed_table_for_pvgen(pv_file)
    feat_table = _make_day_indexed_table_for_tfrecord(ds)
    for key in pvgen_table:
        if key in feat_table:
            rad, feat = sr_model(tf.reshape(
                feat_table[key], (1, len(feat_table[key]))))
            dataset.append({
                "features": feat[0].numpy(),
                "pvgen": [pvgen_table[key]["pvgen"]["value"]]
            })
        else:
            print('pvgen date skiped for ' + str(key))
    return dataset
