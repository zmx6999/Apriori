import itertools
def create_c1(data):
    c1 = []
    _data = []
    for v in data:
        _data.append(frozenset(v))
        for vv in v:
            vv = frozenset([vv])
            if vv not in c1:c1.append(vv)
    return c1,_data


def get_support(data,ck,support):
    t = []
    f = {}
    for v in data:
        for vv in ck:
            if vv.issubset(v):f[vv] = f.get(vv,0)+1
    n = len(data)
    for k in f:
        f[k] = float(f[k])/n
        if f[k] >= support and k not in t:t.append(k)
    return t,f


def join(ck,length):
    _ck = []
    for v in ck:
        for vv in ck:
            m = v.union(vv)
            if len(m) == length and m not in _ck:_ck.append(m)
    return _ck


def subset(v):
    return itertools.chain(*[itertools.combinations(v,i+1) for i,a in enumerate(v)])


def apriori(data,support,confidence):
    ck,_data = create_c1(data)
    _t,_f = get_support(_data,ck,support)
    t,f = _t,_f
    k = 2
    while len(_t) > 0:
        ck = join(ck,k)
        _t,_f = get_support(_data,ck,support)
        t.extend(_t)
        f.update(_f)
        k += 1

    support_data = {}
    for v in t:support_data[tuple(v)] = f[v]

    confidence_data = {}
    for v in t:
        if len(v) > 1:
            ss = subset(list(v))
            for i,sv in enumerate(ss):
                sv = frozenset(sv)
                sd = v.difference(sv)
                if len(sd) > 0:
                    cd = f[v]/f[sv]
                    if cd >= confidence:confidence_data[tuple([tuple(sv),tuple(sd)])] = cd
    return support_data,confidence_data


if __name__ == '__main__':
    data = [v.strip().split(',') for v in open('tesco.csv', 'rU').readlines()]
    support_data, confidence_data = apriori(data,.15,.6)
    print(support_data)
    print(confidence_data)