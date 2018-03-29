import itertools
def create_c1(data):
    c1 = []
    _data = []
    for v in data:
        _data.append(frozenset(v))
        for vv in v:
            vv = frozenset([vv])
            if vv not in c1:
                c1.append(vv)
    return c1,_data


def get_support(data,ck,support):
    t = []
    f = {}
    for v in data:
        for vv in ck:
            if vv.issubset(v):
                f[vv] = f.get(vv,0)+1
    n = len(data)
    for k in f:
        f[k] = float(f[k])/n
        if f[k] >= support:
            t.append(k)
    return t,f


def join(ck,length):
    ck_1 = []
    for v in ck:
        for vv in ck:
            _v = v.union(vv)
            if len(_v) == length and _v not in ck_1:
                ck_1.append(_v)
    return ck_1


def subset(v):
    return itertools.chain(*[itertools.combinations(v,i+1) for i,a in enumerate(v)])


def apriori(data,support,confidence):
    c1,_data = create_c1(data)
    _t,_f = get_support(_data,c1,support)
    t = _t
    f = _f
    k = 2
    while len(_t) > 0:
        ck = join(_t,k)
        _t, _f = get_support(_data, ck, support)
        t.extend(_t)
        f.update(_f)
        k += 1

    support_data = {}
    for v in t:
        support_data[tuple(v)] = f[v]

    confidence_data = {}
    for v in t:
        if len(v) > 1:
            ss = subset(v)
            for sv in ss:
                sv = frozenset(sv)
                sd = v.difference(sv)
                if len(sd) > 0:
                    cd = f[v]/f[sv]
                    if cd >= confidence:
                        confidence_data[tuple([tuple(sv),tuple(sd)])] = cd
    return support_data,confidence_data

if __name__ == '__main__':
    data = [v.strip().split(',') for v in open('tesco.csv').readlines()]
    c1,data = create_c1(data)
    support_data,confidence_data = apriori(data,.15,.6)
    print(support_data)
    print(confidence_data)