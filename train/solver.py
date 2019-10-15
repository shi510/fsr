import os
import math
import itertools
import copy
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import train.util as tutil
import train.input_pipeline as input_pipeline
import preprocessing.convert as convert

def find_best_model(**kwargs):
    epoch = kwargs['epoch']
    batches = kwargs['batch_sizes']
    opts = kwargs['optimizers']
    lrs = kwargs['init_learning_rates']
    models = kwargs['models']
    interestings = kwargs['interestings']
    past_hours = kwargs['past_hours']
    future_hour = kwargs['future_hour']
    train_list = kwargs['train_list']
    test_list = kwargs['test_list']
    log_dir = kwargs['log_dir']
    ablation_report = kwargs['ablation_report']
    
    best_model_param = {
        'learning_rate': 0,
        'batch_size': 0,
        'model': '',
        'opt':'adam'
    }
    best_model = None
    composed = list(itertools.product(batches, zip(opts, lrs), past_hours))
    '''
        find best model, given hyper-parameters.
    '''
    best_loss = 1e+4
    history_collection = []
    
    for model_name in models:
        plt.clf()
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.title(model_name)
        plt.xlabel('Epoch')
        plt.ylabel('Val Loss')
        local_best_hist = None
        local_best_loss = 1e+4
        for param in composed:
            batch_size = param[0]
            opt = param[1][0]
            lr = param[1][1]
            past_hour = param[2]
            cur_setting = '%s_%s_%s'%(batch_size, opt, past_hour)
            dir_name = os.path.join(log_dir, model_name + '_' + cur_setting)
            tutil.make_dir(dir_name)

            train_ds = input_pipeline.DatasetWithParam(
                train_list,
                interestings,
                future_hour,
                past_hour,
                convert.past_pair,
                batch_size
            )
            test_ds = input_pipeline.DatasetWithParam(
                test_list,
                interestings,
                future_hour,
                past_hour,
                convert.past_pair,
                batch_size
            )
            make_model = tutil.get_model(model_name)
            model = make_model(train_ds.features())
            model.compile(
                tf.keras.optimizers.Adam(learning_rate=lr),
                loss={'output':tf.keras.losses.MeanSquaredError()}
            )
            early_stop = tf.keras.callbacks.EarlyStopping(
                patience=10,
                restore_best_weights=True
            )
            print('Try hyper-parameter : ' + cur_setting)
            history = model.fit(
                x=train_ds(),
                validation_data=test_ds(),
                epochs=epoch,
                steps_per_epoch=int(math.floor(len(train_ds) / batch_size)),
                validation_steps=int(math.floor(len(test_ds) / batch_size)),
                callbacks=[early_stop]
            )
            cur_loss = early_stop.best
            file_name = 'best_model' + '_loss=' + format(cur_loss, '.6f') + '.h5'
            model.save(os.path.join(dir_name, file_name))
            
            if best_loss > cur_loss:
                best_model_param['model'] = model_name
                best_model_param['batch_size'] = batch_size
                best_model_param['learning_rate'] = lr
                best_model = model
                best_loss = cur_loss
                best_hist = history.history['val_loss']
                print('best model : ' + cur_setting)
            if local_best_loss > cur_loss:
                local_best_hist = history.history['val_loss']
                local_best_loss = cur_loss
            plt.plot(history.history['val_loss'], label=cur_setting)
        plt.legend(bbox_to_anchor=(1.05, 1, 1.25, 0), loc=1, ncol=3, mode="expand", borderaxespad=0.)
        plt.savefig(os.path.join(log_dir, model_name + '.jpg'))
        history_collection.append((model_name, local_best_hist))
    plt.clf()
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title('Comparing All Best Models')
    plt.xlabel('Epoch')
    plt.ylabel('Val Loss')
    for hist in history_collection:
        plt.plot(hist[1], label=hist[0])
    plt.legend(bbox_to_anchor=(1.05, 1, 1.25, 0), loc=1, ncol=3, mode="expand", borderaxespad=0.)
    plt.savefig(os.path.join(log_dir, 'try_every_hyper_param.jpg'))
    '''
        report ablation study by removing a feature one by one.
    '''
    if ablation_report:
        lr = best_model_param['learning_rate']
        model = best_model_param['model']
        batch_size = best_model_param['batch_size']
        plt.clf()
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.title('Ablation Study')
        plt.xlabel('Epoch')
        plt.ylabel('Val Loss')
        
        # start ablation study with best model.
        print('Start ablation study')
        for key in convert.past_pair['input'].keys():
            past_pair = copy.deepcopy(convert.past_pair)
            past_pair['input'].pop(key)

            train_ds = input_pipeline.DatasetWithParam(
                train_list,
                interestings,
                future_hour,
                past_hour,
                past_pair,
                batch_size
            )
            test_ds = input_pipeline.DatasetWithParam(
                test_list,
                interestings,
                future_hour,
                past_hour,
                past_pair,
                batch_size
            )
            make_model = tutil.get_model(model_name)
            model = make_model(train_ds.features())
            model.compile(
                tf.keras.optimizers.Adam(learning_rate=lr),
                tf.keras.losses.MeanSquaredError()
            )
            print('Try w/o ' + key)
            history = model.fit(
                x=train_ds(),
                validation_data=test_ds(),
                epochs=epoch,
                steps_per_epoch=int(math.floor(len(train_ds) / batch_size)),
                validation_steps=int(math.floor(len(test_ds) / batch_size))
            )
            plt.plot(history.history['val_loss'], label='w/o ' + key)
        plt.legend(bbox_to_anchor=(1.05, 1, 1.25, 0), loc=1, ncol=3, mode="expand", borderaxespad=0.)
        plt.savefig(os.path.join(log_dir, 'ablation.jpg'))
    
    return best_model