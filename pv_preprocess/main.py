import argparse
import os
import common.util as cutil
import pv_preprocess.convert as convert
import tensorflow as tf

parser = argparse.ArgumentParser()
parser.add_argument('tfrecord')
parser.add_argument('-cfg')

def _tf_float_list(value):
    return tf.train.Feature(float_list=tf.train.FloatList(value=value))

def make_tfrecord(sr_file, pv_file, sr_model, future_hour):
    dataset = convert.make_dataset(sr_file, pv_file, sr_model, future_hour)
    file_name = os.path.splitext(os.path.basename(pv_file))[0]
    tf_file = tf.io.TFRecordWriter(file_name+'.tfrecord')
    for data in dataset:
        feature = {
            'features': _tf_float_list(data['features']),
            'pvgen': _tf_float_list(data['pvgen'])
        }
        exam = tf.train.Example(features=tf.train.Features(feature=feature))
        tf_file.write(exam.SerializeToString())
    tf_file.close()

def load_model(model_path, weights_path):
    with open(model_path, 'r') as f:
        content = f.read()
    model = tf.keras.models.model_from_json(content)

    model.load_weights(weights_path)

    return model

if __name__ == '__main__':
    args = parser.parse_args()

    if args.tfrecord:
        cfg = cutil.open_config_file(args.cfg)
        sr_model = load_model(cfg["sr_model_cfg"], cfg["sr_model_weights"])
        make_tfrecord(cfg['sr_tfrecord'], cfg['pv_file'], sr_model,
                      cfg['future_hour'])
        exit()
        print("input size:", convert.size_of_input_transform(cfg["past_hour"]))
