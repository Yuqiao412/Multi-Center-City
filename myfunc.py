def cutoff(name):
    perlist=["110000","310000","440100","440300","120000"]
    if (name in perlist):
        cut=90
    else:
        cut=95
    return cut

def spatialRef(sf):
    f=open(sf,'r')
    result={}
    for line in f.readlines():
        line=line.strip()
        result[line.split(',')[0]]=line.split(',')[1]
    f.close()
    return result

def normalization(data,_max,_min):
    return (data-_min)/(_max-_min)
