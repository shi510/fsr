import argparse
import math
import os
import numpy as np
import tensorflow as tf
import common.util as cutil
import sr_train.solver
import sr_train.visualize as visual
import sr_train.util as tutil

parser = argparse.ArgumentParser()
parser.add_argument('-cfg')

if __name__ == '__main__':
    args = parser.parse_args()
    cfg = cutil.open_config_file(args.cfg)
    model = tutil.get_model(cfg["model"])(cfg["input_size"])
    best_model = sr_train.solver.train(
        model, cfg['train_file'], cfg['test_file'], 
        cfg['learning_rate'], cfg['batch_size'], cfg['epoch'])

    with open('best_model.json', 'w') as f:
        f.write(best_model.to_json())
    best_model.save_weights('best_model_weights.h5')

    # visual.draw_graph(best_model, args['test_list'])
