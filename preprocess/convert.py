import os
from common.registry import Registry
import common.util as cutil
import common.io_register as io_register
import collections
import math
import numpy as np
import datetime

def norm(val, min, max):
    return (val - min) / (max - min)

@io_register.regist_input("일시", past = True)
class CvtDate:

    @classmethod
    def transform(cls, date):
        sp = date.split(' ')
        y = int(sp[0].split('-')[0])
        m = int(sp[0].split('-')[1])
        d = int(sp[0].split('-')[2])
        h = int(sp[1].split(':')[0])
        w = datetime.date(y, m, d).isocalendar()[1]
        
        od = collections.OrderedDict()
        od["weeks1"] = math.sin(w / 53)
        od["weeks2"] = math.cos(w / 53)
        od["hour1"] = math.sin(h / 23)
        od["hour2"] = math.cos(h / 23)
        return od

    @staticmethod
    def size():
        return 4


@io_register.regist_input("기온(°C)", past=True, statistic=True)
class CvtTemp:
    min = -17.2
    max = 37.4

    @classmethod
    def transform(cls, tp):
        name = 'temperature'
        if '' == tp:
            return {name: 0.0}
        else:
            return {name: norm(float(tp), cls.min, cls.max)}

    @staticmethod
    def size():
        return 1


@io_register.regist_input("풍속(m/s)", past=True, statistic=True)
class CvtWS:
    @staticmethod
    def transform(ws):
        name = 'wind_speed'
        if '' == ws:
            return {name: 0.0}
        else:
            val = float(ws)
            if(val == 0):
                return {name: 0}
            elif(val > 0 and val < 4):
                return {name: 0.25}
            elif(val >= 4 and val < 9):
                return {name: 0.5}
            elif(val >= 9 and val < 14):
                return {name: 0.75}
            else:
                return {name: 1.}

    @staticmethod
    def size():
        return 1


@io_register.regist_input("습도(%)", past=True, statistic=True)
class CvtRH:
    min = 0
    max = 100
    @classmethod
    def transform(cls, rh):
        name = 'humidity'
        if '' == rh:
            return {name: 0.0}
        else:
            return {name: norm(float(rh), cls.min, cls.max)}

    @staticmethod
    def size():
        return 1


@io_register.regist_input("전운량(10분위)", past=True, statistic=True)
class CvtCC:
    @staticmethod
    def transform(cc):
        name = 'cloud_cover'
        if '' == cc:
            return {name: 0.0}
        else:
            val = float(cc)
            if(val == 0):
                return {name: 0}
            elif(val > 0 and val < 6):
                return {name: 0.3}
            elif(val >= 6 and val < 9):
                return {name: 0.6}
            else:
                return {name: 1.}

    @staticmethod
    def size():
        return 1


@io_register.regist_input("강수량(mm)", past=True, statistic=True)
class CvtPCT:
    min = 0
    max = 56.5

    @classmethod
    def transform(cls, pc):
        name = 'precipitation'
        if '' == pc:
            return {name: 0.0}
        else:
            return {name: norm(float(pc), cls.min, cls.max)}

    @staticmethod
    def size():
        return 1


@io_register.regist_input("적설(cm)", past=True, statistic=True)
class CvtPCT:
    min = 0
    max = 100

    @classmethod
    def transform(cls, pc):
        name = 'snow'
        if '' == pc:
            return {name: 0.0}
        else:
            return {name: norm(float(pc), cls.min, cls.max)}

    @staticmethod
    def size():
        return 1


# @io_register.regist_input("이슬점온도(°C)", past=True, statistic=True)
class CvtDew:
    min = -28.2
    max = 27.3

    @classmethod
    def transform(cls, dew):
        name = 'dew'
        if '' == dew:
            return {name: 0.0}
        else:
            return {name: norm(float(dew), cls.min, cls.max)}

    @staticmethod
    def size():
        return 1


# @io_register.regist_input("풍향(16방위)", past=True, statistic=True)
class CvtWindDir:
    min = 0
    max = 360

    @classmethod
    def transform(cls, wd):
        name = ''
        if '' == wd:
            return {name: 0.0}
        else:
            return {name: norm(float(wd), cls.min, cls.max)}

    @staticmethod
    def size():
        return 1


@io_register.regist_output("일사(MJ/m2)", future=True, statistic=True)
class CvtRAD:
    min = 0
    max = 4.07

    @classmethod
    def transform(cls, rad):
        name = 'radiation'
        if '' == rad:
            return {name: 0.0}
        else:
            return {name: norm(float(rad), cls.min, cls.max)}

    @classmethod
    def denorm(cls, norm_rad):
        return norm_rad * (cls.max - cls.min) + cls.min

    @staticmethod
    def size():
        return 1

def size_of_input_transform(past_hour):
    accum = 0
    for key in Registry.REGISTRY_LIST:
        fn = Registry.REGISTRY_LIST[key]["fn"]
        past = Registry.REGISTRY_LIST[key]["past"]
        if Registry.REGISTRY_LIST[key]["io_type"] == "input":
            size = fn.size()*(past_hour+1) if past else fn.size()
            accum += size
    return accum

def _make_day_indexed_table(csv_list):
    root_path = os.path.dirname(csv_list)
    files = cutil.read_lines_from_file(csv_list, root_path, 'utf-8')

    def day2int(str):
        sp = str.split(' ')
        y = sp[0].split('-')[0]
        m = sp[0].split('-')[1]
        d = sp[0].split('-')[2]
        h = sp[1].split(':')[0]
        return int(y + m + d), int(h)

    table = {}
    for file in files:
        f = open(file, 'r', encoding='euc-kr')
        title = cutil.remove_cr(f.readline()).split(',')
        while True:
            vals = cutil.remove_cr(f.readline()).split(',')
            if len(vals) == 1:
                break
            try:
                idx = title.index("일시")
            except:
                raise 'Not found ' + "일시"
            day, hour = day2int(vals[idx])
            attrs = {}
            for key in Registry.REGISTRY_LIST:
                try:
                    idx = title.index(key)
                except:
                    raise 'Not found ' + key
                attrs[key] = {
                    "value": vals[idx]
                }
            if day in table:
                table[day][hour] = attrs
            else:
                table[day] = {}
        f.close()
    return table

def make_dataset(csv_list, past_hour, future_hour, start, end):
    dataset=[]
    table = _make_day_indexed_table(csv_list)
    time_size = past_hour+1
    expected_input_size = 0
    for key in Registry.REGISTRY_LIST:
        fn = Registry.REGISTRY_LIST[key]["fn"]
        io_type = Registry.REGISTRY_LIST[key]["io_type"]
        if io_type == "input":
            expected_input_size += fn.size() * time_size
    for d in table:
        for h in range(start, end + 1):
            input_pack = {}
            output_pack = []
            for key in Registry.REGISTRY_LIST:
                fn = Registry.REGISTRY_LIST[key]["fn"]
                io_type = Registry.REGISTRY_LIST[key]["io_type"]
                past = Registry.REGISTRY_LIST[key]["past"]
                future = Registry.REGISTRY_LIST[key]["future"]
                phour = past_hour if past else 0
                fhour = future_hour if future else 0
                if io_type == "input":
                    try:
                        for n in range(h, h-phour-1, -1):
                            value = fn.transform(table[d][n][key]["value"])
                            for name in value:
                                if key in input_pack:
                                    input_pack[key].append(value[name])
                                else:
                                    input_pack[key] = [value[name]]
                    except:
                        print("[Warning] Skip: ", d, h)
                        break
                elif io_type == "output":
                    try:
                        value = fn.transform(table[d][h+fhour][key]["value"])
                    except:
                        print("[Warning] Skip: ", d, h)
                        break
                    for name in value:
                        output_pack.append(value[name])
            size = 0
            for key in input_pack:
                data = input_pack[key]
                size += len(data)
            if expected_input_size == size and len(output_pack) > 0:
                arr = []
                for t in range(time_size):
                    for key in input_pack:
                        fn = Registry.REGISTRY_LIST[key]["fn"]
                        feat_size = fn.size()
                        data = input_pack[key]
                        arr = arr + data[t*feat_size:(t+1)*feat_size]
                        print(key, t)
                exit(1)
                dataset.append({
                    "date": [int(str(d)+str(h).zfill(2))],
                    "features": arr,
                    "radiation": output_pack
                })
    return dataset
