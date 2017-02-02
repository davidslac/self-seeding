from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import Counter
from pprint import pprint

import psana
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

# in amoi0314 - we need runs from 12-06 14:41:12, recording data in the 
# sxr spectrometer. L3 is 3402

# then at 14:44 - says dataa recorded into diamcc14

# In the amo

def count_data(ds, limit=0):
    epics = Counter()
    data = Counter()

    estore = ds.env().epicsStore()
    for name in estore.pvNames():
        epics[name] += 1

    for idx, evt in enumerate(ds.events()):
        for key in evt.keys():
            data[str(key)] += 1
        if limit > 0 and idx > limit:
            break

    return epics, data

def look_at_keys():
    for run in range(282, 291):
        runstr = 'exp=diamcc14:run=%d' % run
        try:
            ds = psana.DataSource(runstr)
        except Exception, exp:
            print("unable to open %s" % runstr)
            print(exp)
            continue
        epics, data = count_data(ds, limit=0)
        print("========= %s ========" % runstr)
        print("-- epics --")
        pprint(dict(epics))
        print("-- data --")
        pprint(dict(data))

def look_at_spectrometer():
    plt.figure(1)
    for run in range(282, 291):
        runstr = 'exp=diamcc14:run=%d' % run
        try:
            ds = psana.DataSource(runstr)
        except Exception, exp:
            print("unable to open %s" % runstr)
            print(exp)
            continue
        for evt in ds.events():
            opal = evt.get(psana.Camera.FrameV1, psana.Source('DetInfo(XrayTransportDiagnostic.20:Opal1000.0)'))
            if None is opal: continue
            MX=500
            plt.imshow(np.minimum(MX,np.maximum(0,opal.data16().astype(np.float))), vmin=0, vmax=MX, interpolation='none')
            plt.show()
            plt.pause(.1)
            raw_input('hi')
            
if __name__ == '__main__':
#    look_at_keys()
    look_at_spectrometer()
    
