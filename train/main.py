import argparse
import math
import os
import numpy as np
import tensorflow as tf
import common.util as cutil
import train.util as tutil
import train.solver

parser = argparse.ArgumentParser()
parser.add_argument('--config_file')

if __name__ == '__main__':
    args = parser.parse_args()
    args = cutil.open_config_file(args.config_file)

    best_model = train.solver.find_best_model(
        batch_sizes=args['batch_sizes'],
        models=args['models'],
        optimizers=['adam'],
        init_learning_rates=[1e-4],
        epoch=args['epoch'],
        interestings=args['interestings'],
        past_hours=args['past_hours'],
        ablation_report=True,
        train_list=args['train_list'],
        test_list=args['test_list'],
        log_dir='logs'
    )

    with open('best_model.json', 'w') as f:
        f.write(best_model.to_json())
    best_model.save_weights('best_model_weights.h5')
