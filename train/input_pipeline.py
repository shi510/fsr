import tensorflow as tf
import train.util as tutil

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