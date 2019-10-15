import tensorflow as tf
import train.util as tutil
import preprocessing.util as putil
import preprocessing.statistic as statistic
import preprocessing.convert as convert

class Dataset:
    
    def __init__(self, path, batch_size):
        data = tutil.read_train_data(path)
        x = []
        y = []
        for line in data:
            x.append(line[:-1])
            y.append([line[-1]])
        self.num_features = len(x[0])
        self.num_samples = len(x)
        self.ds = tf.data.Dataset.from_tensor_slices((x, y))
        self.ds = self.ds.repeat()
        self.ds = self.ds.shuffle(1000)
        self.ds = self.ds.batch(batch_size)
        self.ds = self.ds.prefetch(1000)

    def __len__(self):
        return self.num_samples

    def __call__(self):
        return self.ds

    def features(self):
        return self.num_features

class DatasetWithParam:
    
    def __init__(self, file, interestings, future_hour, past_hour, past_pair, batch_size):
        x, y = self._prepare_data(file, interestings, future_hour, past_hour, past_pair)
        self.num_features = len(x[0])
        self.num_samples = len(x)
        self.ds = tf.data.Dataset.from_tensor_slices((x, y))
        self.ds = self.ds.repeat()
        self.ds = self.ds.shuffle(1000)
        self.ds = self.ds.batch(batch_size)
        self.ds = self.ds.prefetch(1000)

    def __len__(self):
        return self.num_samples

    def __call__(self):
        return self.ds

    def _prepare_data(self, file, interestings, future_hour, past_hour, past_pair):
        dict_list = putil.convert_csv2dict_list(file, interestings)
        dict_list = statistic.normalize(dict_list, convert.norm_lambdas)
        x_, y_ = putil.make_past_pair(dict_list, future_hour, past_hour, past_pair)
        x = []
        y = []
        for a, b in zip(x_, y_):
            input = []
            for name in a:
                input.append(a[name])
            x.append(input)
            y.append(b)
        return x, y

    def features(self):
        return self.num_features