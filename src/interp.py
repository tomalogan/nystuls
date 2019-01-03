#!/usr/bin/python

def interp(lo,hi,val,valmax):
    lo = float(lo)
    hi = float(hi)
    val = float(val)
    valmax = float(valmax)
    spread = hi - lo
    pct = val/valmax
    interp = lo + pct*spread
    return(int(interp))


