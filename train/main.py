import argparse
import math
import os
import numpy as np
import tensorflow as tf
import common.util as cutil
import train.solver

parser = argparse.ArgumentParser()
sub_parser = parser.add_subparsers(dest='cmd')
train_parser = sub_parser.add_parser('train')
train_parser.add_argument('-cfg')
weights_parser = sub_parser.add_parser('input_weights')
weights_parser.add_argument('-cfg')


def load_model(model_name):
    with open(model_name+'.json', 'r') as f:
        content = f.read()
    model = tf.keras.models.model_from_json(content)
    model.load_weights(model_name+'.h5')
    return model

if __name__ == '__main__':
    args = parser.parse_args()
    if args.cmd == 'train':
        cfg = cutil.open_config_file(args.cfg)
        best_model = train.solver.train(
            cfg['model'], cfg['input_size'], cfg['train_file'], cfg['test_file'],
            cfg['learning_rate'], cfg['batch_size'], cfg['epoch'])

        with open('best_model.json', 'w') as f:
            f.write(best_model.to_json())
        best_model.save_weights('best_model.h5')
    if args.cmd == 'input_weights':
        cfg = cutil.open_config_file(args.cfg)
        best_model = load_model('best_model')
        weights = train.solver.calc_inputs_weight(best_model, cfg['train_file'], cfg['input_size'])
        print(weights)

    # visual.draw_graph(best_model, cfg['test_file'])
