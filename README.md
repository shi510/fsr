# FSR  
This project is for Forecasting Solar Radiation.  
The data format that is used in this project is based on the format of Korea Meteorological Administration (KMA).  
For example, we have csv file as below.  

| Observatory #|   Date   | Temperature | Precipitation | Wind Speed | ... |
|:------------:|:--------:|:-----------:|:-------------:|:----------:|:---:|
|     123      |2000-01-01|      30     |       5       |     7.2    | ... |

## Prepare Your Train/Test Data
You can download 1-hour-interval meteorological data from KMA.  
```
1. Go to https://data.kma.go.kr.  
2. Select Your interesting Regions.  
3. Select 1-hour-interval-data.  
4. Select all meteorological data. (Ex: Temperature, Wind, Relative Humidity ...)  
5. Download 2010-01-01 ~ Current Date.  
```
Next step is to split the files into train and test data.  
```
1. Create folders : train and test.  
2. Move meteorological data files (2010-01-01 ~ 2017-12-31) to train folder.  
3. Move meteorological data files (2018-01-01 ~ Current Date) to test folder.  
4. Create train list file.  
5. Create test list file.  
```
We have folder structure as below.  
```
fsr  
  |-- region1  
  |         |-- train  
  |         |       |-- 2010.csv  
  |         |       |-- 2011.csv  
  |         |       |-- ...  
  |         |-- test  
  |         |       |-- 2018.csv  
  |         |       |-- 2019.csv  
  |-- region1_train.txt  
  |-- region1_test.txt  
```
The region1_train.txt format is as below.  
```
region1/train/2010.csv  
region1/train/2011.csv  
...
```
The region1_test.txt format is as below.  
```
region1/test/2018.csv  
region1/test/2019.csv  
```

## How To Make TFRecord From Your Train/Test List File  
Before run the python script, you have to add fsr's absolute path to PYTHONPATH.  
For example,  
```
1. Open terminal in fsr folder.  
2. Do command, 
   in windows, $env:PYTHONPATH=$pwd  
   in unix-like cmd, export PYTHONPATH=$(pwd) 
```
```
1. Modify preprocess/args.json.  
    "files" : [  
      "/path/to/your/region1_train.txt",  
      "/path/to/your/region1_test.txt"  
    ],  
2. Then, try the command below.  
  python preprocess/main.py tfrecord -cfg preprocess/args.json  
```

## How To Train Your Forecasting Model  
```
1. Modify train/args.json.  
  "train_file" : "/path/to/your/region1_train.tfrecord",  
  "test_file" : "/path/to/your/region1_test.tfrecord",  
    ...  
2. Then, try the command below.  
  python train/main.py train -cfg='train/args.json'.  
```