"""
date_str: '0000-00-00 00:00'
return [month, day, hour(24)] as type[float, float, float]
"""
def cvt_date(date):
    sp = date.split(' ')
    m = float(sp[0].split('-')[1])
    d = float(sp[0].split('-')[2])
    h = float(sp[1].split(':')[0])
    return {'월': m, '일': d, '시': h}

def cvt_temperature(tp):
    name = '기온'
    if '' == tp:
        return {name: 0.0}
    else:
        return {name: float(tp)}

def cvt_wind_speed(ws):
    name = '풍속'
    if '' == ws:
        return {name: 0.0}
    else:
        return {name: float(ws)}

def cvt_relative_humidity(rh):
    name = '습도'
    if '' == rh:
        return {name: 0.0}
    else:
        return {name: float(rh)}

def cvt_cloud_cover(cc):
    name = '운량'
    if '' == cc:
        return {name: 0.0}
    else:
        return {name: float(cc)}

def cvt_radiation(rad):
    name = '일사량'
    if '' == rad:
        return {name: 0.0}
    else:
        return {name: float(rad)}

norm_lambdas = {
    '월': lambda x: x/12,
    '일': lambda x: x/31,
    '시': lambda x: x/23,
    '기온': lambda x: (x+12.3)/(37.1+12.3),
    '풍속': lambda x: x/16.3,
    '습도': lambda x: x/100,
    '운량': lambda x: x/10,
    '일사량': lambda x: x/4.6
}

past_pair = {
    'input': {
        '월': False,
        '일': False,
        '시': False,
        '기온': True, 
        '풍속': True,
        '습도': True,
        '운량': True
    },
    'output': '일사량'
}