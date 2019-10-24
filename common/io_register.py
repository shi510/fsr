import functools
from common.registry import Registry

class IORegister:

    def __init__(self, key_name, io_type, past=False, future=False):
        self.key_name = key_name
        self.io_type = io_type
        self.past = past
        self.future = future

    def __call__(self, fn):
        Registry.REGISTRY_LIST[self.key_name] = {
            "fn": fn,
            "io_type": self.io_type,
            "past": self.past,
            "future": self.future
        }

regist_input = functools.partial(IORegister, io_type="input")
regist_output = functools.partial(IORegister, io_type="output")
