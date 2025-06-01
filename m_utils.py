from typing import Iterable,Dict
def iter2str(it:Iterable):
    res = ""
    it_1 = it.items() if isinstance(it,Dict) else it
    for x in it_1:
        if isinstance(x,str):
           res += x
        elif not isinstance(x,Iterable):
            res += str(x)
        else:
            res += iter2str(x)
        res += ","
    return res[:-1]