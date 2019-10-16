import importlib
import os
from pathlib import Path
import common.util as cutil

def get_model(model_type):
    return getattr(importlib.import_module('model'), model_type)

def make_dir(path):
    dir = Path(path)
    dir.mkdir(parents=True, exist_ok=True)