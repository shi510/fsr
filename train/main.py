import argparse
import math
import os
import numpy as np
import tensorflow as tf
import common.util as cutil
import train.solver

parser = argparse.ArgumentParser()
parser.add_argument('-cfg')

if __name__ == '__main__':
    args = parser.parse_args()
    cfg = cutil.open_config_file(args.cfg)
    best_model = train.solver.train(
        cfg["model"], cfg["input_size"], cfg['train_file'], cfg['test_file'],
        cfg['learning_rate'], cfg['batch_size'], cfg['epoch'])

    with open('best_model.json', 'w') as f:
        f.write(best_model.to_json())
    best_model.save_weights('best_model_weights.h5')

    # visual.draw_graph(best_model, args['test_list'])
