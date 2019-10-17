import importlib
import os
from pathlib import Path
import common.util as cutil

def get_model(model_type):
    as_file = model_type.rpartition('.')[0]
    as_fn = model_type.rpartition('.')[2]
    return getattr(importlib.import_module(as_file), as_fn)

def make_dir(path):
    dir = Path(path)
    dir.mkdir(parents=True, exist_ok=True)