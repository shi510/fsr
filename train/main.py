import argparse
import math
import os
import numpy as np
import tensorflow as tf
import common.util as cutil
import train.util as tutil
import input_pipeline

parser = argparse.ArgumentParser()
parser.add_argument('--config_file')

if __name__ == '__main__':
    args = parser.parse_args()
    args = cutil.open_config_file(args.config_file)

    train_ds = input_pipeline.Dataset(
        args['train_list'],
        args['batch_size']
    )

    test_ds = input_pipeline.Dataset(
        args['test_list'],
        args['batch_size']
    )

    model = tutil.get_model(args['model'])
    model = model(train_ds.features())
    loss = tf.keras.losses.MeanSquaredError()

    writer = tf.summary.create_file_writer('logs')
    opt = tf.keras.optimizers.Adam(learning_rate=1e-4)

    model.compile(opt, loss)

    model.fit(x = train_ds(),
        validation_data = test_ds(),
        epochs = args['epoch'],
        steps_per_epoch = int(math.floor(len(train_ds) / args['batch_size'])),
        validation_steps = int(math.floor(len(test_ds) / args['batch_size']))
    )