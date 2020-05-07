import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers

def model1(num_features, name="model"):
    input = tf.keras.Input(num_features)
    output = layers.Dense(40)(input)
    output = layers.BatchNormalization()(output)
    output = layers.LeakyReLU()(output)
    output = layers.Dense(20, name="features")(output)
    features = output
    output = layers.BatchNormalization()(output)
    output = layers.LeakyReLU()(output)
    output = layers.Dense(1, activation='sigmoid', name='output')(output)
    return tf.keras.Model(input, [output, features], name=name)

def model2(num_features, name="model"):
    input = tf.keras.Input(num_features)
    output = layers.Dense(15)(input)
    output = layers.BatchNormalization()(output)
    output = layers.LeakyReLU()(output)
    output = layers.Dense(15, name="features")(output)
    features = output
    output = layers.BatchNormalization()(output)
    output = layers.LeakyReLU()(output)
    output = layers.Dense(1, activation='sigmoid', name='output')(output)
    return tf.keras.Model(input, [output, features], name=name)

def model3(num_features, name="model"):
    input = tf.keras.Input(num_features)
    output = layers.Reshape((num_features, 1))(input)
    output = _inception(output, 12)
    output = _res_inception(output, 12)
    output = _res_inception(output, 12)
    output = _res_inception(output, 12)
    output = layers.Flatten()(output)
    output = layers.Dense(64)(output)
    output = layers.BatchNormalization()(output)
    output = layers.LeakyReLU()(output)
    output = layers.Dense(24, name="features")(output)
    features = output
    output = layers.BatchNormalization()(output)
    output = layers.LeakyReLU()(output)
    output = layers.Dense(1, activation='sigmoid', name='output')(output)
    return tf.keras.Model(input, [output, features], name=name)

def _inception(x, filters):
    c3 = layers.Conv1D(filters, 3, padding='same')(x)
    c3 = layers.BatchNormalization()(c3)
    c3 = layers.LeakyReLU()(c3)

    c5 = layers.Conv1D(filters, 5, padding='same')(x)
    c5 = layers.BatchNormalization()(c5)
    c5 = layers.LeakyReLU()(c5)

    c7 = layers.Conv1D(filters, 7, padding='same')(x)
    c7 = layers.BatchNormalization()(c7)
    c7 = layers.LeakyReLU()(c7)

    output = layers.Concatenate()([c3, c5, c7])
    return output

def _res_inception(x, filters):
    shortcut = x
    x = _inception(x, filters)
    x = layers.Add()([x, shortcut])
    return x

def model4(num_features):
    input = tf.keras.Input(num_features)
    output = layers.GRU(48)(input)
    output = layers.Dense(24)(output)
    output = layers.LeakyReLU()(output)
    output = layers.Dense(12)(output)
    features = output
    output = layers.LeakyReLU()(output)
    output = layers.Dense(1, activation='sigmoid', name='output')(output)
    return tf.keras.Model(input, [output, features])
