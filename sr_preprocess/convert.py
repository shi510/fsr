import os
from common.registry import Registry
import common.util as cutil
import common.io_register as io_register

def norm(val, min, max):
    return (val - min) / (max - min)

"""
date_str: '0000-00-00 00:00'
return [month, day, hour(24)] as type[float, float, float]
"""
def cvt_date(date):
    sp = date.split(' ')
    m = float(sp[0].split('-')[1])
    # d = float(sp[0].split('-')[2])
    h = float(sp[1].split(':')[0])
    return {'month': m, 'hour': h}

@io_register.regist_input("일시")
class CvtDate:
    m_min = 1
    m_max = 12
    h_min = 0
    h_max = 23

    @classmethod
    def transform(self, date):
        sp = date.split(' ')
        m = float(sp[0].split('-')[1])
        # d = float(sp[0].split('-')[2])
        h = float(sp[1].split(':')[0])
        m = norm(m, self.m_min, self.m_max)
        h = norm(h, self.h_min, self.h_max)
        return {'month': m, 'hour': h}

    @staticmethod
    def size():
        return 2

def cvt_temperature(tp):
    name = 'temperature'
    if '' == tp:
        return {name: 0.0}
    else:
        return {name: float(tp)}


@io_register.regist_input("기온(°C)", past=True)
class CvtTemp:
    min = -12.3
    max = 37.1

    @classmethod
    def transform(self, tp):
        name = 'temperature'
        if '' == tp:
            return {name: 0.0}
        else:
            return {name: norm(float(tp), self.min, self.max)}

    @staticmethod
    def size():
        return 1

def cvt_wind_speed(ws):
    name = 'wind_speed'
    if '' == ws:
        return {name: 0.0}
    else:
        val = float(ws)
        if(val >= 0 and val < 4):
            return {name: 0.}
        elif(val >= 4 and val < 9):
            return {name: 0.3}
        elif(val >= 9 and val < 14):
            return {name: 0.7}
        else:
            return {name: 1.}


@io_register.regist_input("풍속(m/s)", past=True)
class CvtWS:
    @staticmethod
    def transform(ws):
        name = 'wind_speed'
        if '' == ws:
            return {name: 0.0}
        else:
            val = float(ws)
            if(val >= 0 and val < 4):
                return {name: 0.}
            elif(val >= 4 and val < 9):
                return {name: 0.3}
            elif(val >= 9 and val < 14):
                return {name: 0.7}
            else:
                return {name: 1.}

    @staticmethod
    def size():
        return 1

def cvt_relative_humidity(rh):
    name = 'humidity'
    if '' == rh:
        return {name: 0.0}
    else:
        return {name: float(rh)}


@io_register.regist_input("습도(%)", past=True)
class CvtRH:
    min = 0
    max = 100
    @classmethod
    def transform(self, rh):
        name = 'humidity'
        if '' == rh:
            return {name: 0.0}
        else:
            return {name: norm(float(rh), self.min, self.max)}

    @staticmethod
    def size():
        return 1

def cvt_cloud_cover(cc):
    name = 'cloud_cover'
    if '' == cc:
        return {name: 0.0}
    else:
        val = float(cc)
        if(val >= 0 and val < 6):
            return {name: 0.}
        elif(val >= 6 and val < 9):
            return {name: 0.5}
        else:
            return {name: 1.}

@io_register.regist_input("전운량(10분위)", past=True)
class CvtCC:
    @staticmethod
    def transform(cc):
        name = 'cloud_cover'
        if '' == cc:
            return {name: 0.0}
        else:
            val = float(cc)
            if(val >= 0 and val < 6):
                return {name: 0.}
            elif(val >= 6 and val < 9):
                return {name: 0.5}
            else:
                return {name: 1.}

    @staticmethod
    def size():
        return 1

def cvt_precipitation(pc):
    name = 'precipitation'
    if '' == pc:
        return {name: 0.0}
    else:
        return {name: float(pc)}

@io_register.regist_input("강수량(mm)", past=True)
class CvtPCT:
    min = 0
    max = 73.5

    @classmethod
    def transform(self, pc):
        name = 'precipitation'
        if '' == pc:
            return {name: 0.0}
        else:
            return {name: norm(float(pc), self.min, self.max)}

    @staticmethod
    def size():
        return 1

def cvt_radiation(rad):
    name = 'radiation'
    if '' == rad:
        return {name: 0.0}
    else:
        return {name: float(rad)}

@io_register.regist_output("일사(MJ/m2)", future=True)
class CvtRAD:
    min = 0
    max = 4.6

    @classmethod
    def transform(self, rad):
        name = 'radiation'
        if '' == rad:
            return {name: 0.0}
        else:
            return {name: norm(float(rad), self.min, self.max)}

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

def make_dataset(csv_list, past_hour, future_hour, start, end):
    root_path = os.path.dirname(csv_list)
    files = cutil.read_lines_from_file(csv_list, root_path, 'utf-8')
    inputs = []
    outputs = []
    table = {}

    def day2int(str):
        sp = str.split(' ')
        y = sp[0].split('-')[0]
        m = sp[0].split('-')[1]
        d = sp[0].split('-')[2]
        h = sp[1].split(':')[0]
        return int(y + m + d), int(h)

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
    for d in table:
        for h in range(start, end + 1):
            input_pack = []
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
                                input_pack.append(value[name])
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
            if len(input_pack) > 0 and len(output_pack) > 0:
                inputs.append(input_pack)
                outputs.append(output_pack)
    return inputs, outputs

norm_lambdas = {
    'month': lambda x: x/12,
    # 'day': lambda x: x/31,
    'hour': lambda x: x/23,
    'temperature': lambda x: (x+12.3)/(37.1+12.3),
    'wind_speed': lambda x: x/16.3,
    'humidity': lambda x: x/100,
    'cloud_cover': lambda x: x,
    'precipitation': lambda x: x/73.5,
    'radiation': lambda x: x/4.6
}

past_pair = {
    'input': {
        'month': False,
        # 'day': False,
        'hour': False,
        'temperature': True, 
        'wind_speed': True,
        'humidity': True,
        'cloud_cover': True,
        'precipitation': True
    },
    'output': 'radiation'
}
