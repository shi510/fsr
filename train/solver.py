import math
import numpy as np
import tensorflow as tf
import train.util as tutil

def _parse(x_shape):
    def map_fn(proto):
        feature_disc = {
            "date": tf.io.FixedLenFeature([], tf.int64),
            'features': tf.io.FixedLenSequenceFeature([], tf.float32, allow_missing=True),
            'radiation': tf.io.FixedLenFeature([], tf.float32)
        }
        exam = tf.io.parse_single_example(proto, feature_disc)
        return tf.reshape(exam['features'], x_shape), exam['radiation']
    return map_fn

def make_dataset(tfrecord_file, batch, input_shape):
    size = sum(1 for _ in tf.data.TFRecordDataset(tfrecord_file))
    ds = tf.data.TFRecordDataset(tfrecord_file)
    ds = ds.map(_parse(input_shape))
    ds = ds.repeat()
    ds = ds.shuffle(size)
    ds = ds.batch(batch)
    ds = ds.prefetch(size)
    return ds, size

def train(model_name, input_shape, train_file, test_file, lr, batch=2048, epoch=50):
    model = tutil.get_model(model_name)(input_shape)
    train_ds, train_size = make_dataset(train_file, batch, input_shape)
    test_ds, test_size = make_dataset(test_file, batch, input_shape)
    model.compile(
        tf.keras.optimizers.Adam(learning_rate=lr),
        loss={'output': tf.keras.losses.MeanSquaredError()}
    )
    early_stop = tf.keras.callbacks.EarlyStopping(
        patience=10,
        restore_best_weights=True
    )
    history = model.fit(
        x=train_ds,
        validation_data=test_ds,
        epochs=epoch,
        steps_per_epoch=int(math.floor(train_size / batch)),
        validation_steps=int(math.floor(test_size / batch)),
        callbacks=[early_stop]
    )
    return model

def calc_inputs_weight(model, data_file, shape, batch=512, eps=1e-3):
    ds = tf.data.TFRecordDataset(data_file)
    ds = ds.map(_parse(shape))
    ds = ds.batch(batch, drop_remainder=True)
    size = np.array(shape).prod()
    diffs = np.zeros((size))
    for x, y in ds:
        for n in range(size):
            tp = np.reshape(x.numpy().copy(), (-1, size))
            tn = np.reshape(x.numpy().copy(), (-1, size))
            tp[:,n] += eps
            tn[:,n] -= eps
            fp = model(np.reshape(tp, [-1] + shape))[0]
            fn = model(np.reshape(tn, [-1] + shape))[0]
            diffs[n] += np.sum(np.abs((fp-fn)/(2*eps)))
    return np.array(diffs / np.sum(diffs)).reshape(shape)
