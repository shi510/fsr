"""
date_str: '0000-00-00 00:00'
return [month, day, hour(24)] as type[float, float, float]
"""
def cvt_date(date):
    sp = date.split(' ')
    m = float(sp[0].split('-')[1])
    d = float(sp[0].split('-')[2])
    h = float(sp[1].split(':')[0])
    return {'month': m, 'day': d, 'hour': h}

def cvt_temperature(tp):
    name = 'temperature'
    if '' == tp:
        return {name: 0.0}
    else:
        return {name: float(tp)}

def cvt_wind_speed(ws):
    name = 'wind_speed'
    if '' == ws:
        return {name: 0.0}
    else:
        return {name: float(ws)}

def cvt_relative_humidity(rh):
    name = 'humidity'
    if '' == rh:
        return {name: 0.0}
    else:
        return {name: float(rh)}

def cvt_cloud_cover(cc):
    name = 'cloud_cover'
    if '' == cc:
        return {name: 0.0}
    else:
        return {name: float(cc)}

def cvt_precipitation(pc):
    name = 'precipitation'
    if '' == pc:
        return {name: 0.0}
    else:
        return {name: float(pc)}

def cvt_radiation(rad):
    name = 'radiation'
    if '' == rad:
        return {name: 0.0}
    else:
        return {name: float(rad)}

norm_lambdas = {
    'month': lambda x: x/12,
    'day': lambda x: x/31,
    'hour': lambda x: x/23,
    'temperature': lambda x: (x+12.3)/(37.1+12.3),
    'wind_speed': lambda x: x/16.3,
    'humidity': lambda x: x/100,
    'cloud_cover': lambda x: x/10,
    'precipitation': lambda x: x/73.5,
    'radiation': lambda x: x/4.6
}

past_pair = {
    'input': {
        'month': False,
        'day': False,
        'hour': False,
        'temperature': True, 
        'wind_speed': True,
        'humidity': True,
        'cloud_cover': True,
        'precipitation': True
    },
    'output': 'radiation'
}