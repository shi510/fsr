def find_min_max(lines, target, init_min=9999, init_max=-9999):
    min = init_min
    max = init_max
    
    for l in lines:
        if min > l[target]:
            min = l[target]
        elif max < l[target]:
            max = l[target]
    
    return min, max

def print_statistics(dict_list):
    names = dict_list[0].keys()
    for name in names:
        min, max = find_min_max(dict_list, name)
        print('{} => Min: {}, Max: {}'.format(name, min, max))

def normalize(dict_list, norm_fns):
    for line in dict_list:
        for name in line:
            line[name] = norm_fns[name](line[name])
    return dict_list