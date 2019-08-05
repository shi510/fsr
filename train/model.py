import tensorflow as tf
import tensorflow.keras.layers as layers

def model1(num_features):
    input = tf.keras.Input([num_features])
    output = layers.Dense(256, layers.LeakyReLU())(input)
    output = layers.Dense(64, layers.LeakyReLU())(output)
    output = layers.Dense(1)(output)
    return tf.keras.Model(input, output)

def model2(num_features):
    input = tf.keras.Input([num_features])
    output = _dense_bn_act(input, 256, layers.LeakyReLU())
    output = _dense_bn_act(output, 64, layers.LeakyReLU())
    output = layers.Dense(1)(output)
    return tf.keras.Model(input, output)

def _dense_bn_act(input, units, act):
    output = layers.Dense(units, use_bias=False)(input)
    output = layers.BatchNormalization()(output)
    output = act(output)
    return output

def model3(num_features):
    input = tf.keras.Input((num_features))
    output = layers.Reshape((num_features, 1))(input)
    output = _inception(output, 10)
    output = _res_inception(output, 10)
    output = _res_inception(output, 10)
    output = layers.Flatten()(output)
    output = layers.Dense(128, activation=layers.LeakyReLU())(output)
    output = layers.Dropout(0.5)(output)
    output = layers.Dense(32, activation=layers.LeakyReLU())(output)
    output = layers.Dropout(0.1)(output)
    output = layers.Dense(1)(output)
    return tf.keras.Model(input, output)

def _inception(x, filters):
    act = layers.LeakyReLU()
    c3 = layers.Conv1D(filters, 3, padding='same', activation=act)(x)
    c5 = layers.Conv1D(filters, 5, padding='same', activation=act)(x)
    c7 = layers.Conv1D(filters, 7, padding='same', activation=act)(x)
    output = layers.Concatenate()([c3, c5, c7])
    return output

def _res_inception(x, filters):
    shortcut = x
    x = _inception(x, filters)
    x = layers.Add()([x, shortcut])
    return x