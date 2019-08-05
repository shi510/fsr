import importlib
import common.util as cutil

def get_model(model_type):
    as_file = model_type.rpartition('.')[0]
    as_fn = model_type.rpartition('.')[2]
    return getattr(importlib.import_module(as_file), as_fn)

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