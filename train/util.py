import importlib
import common.util as cutil

def get_model(model_type):
    return getattr(importlib.import_module('model'), model_type)

def read_train_data(file_name):
    train_data = []
    with open(file_name, 'r') as f:
        while True:
            line = cutil.remove_cr(f.readline())
            if line == '':
                break
            sub = []
            for elem in line.split(' '):
                sub.append(float(elem))
            train_data.append(sub)
    return train_data