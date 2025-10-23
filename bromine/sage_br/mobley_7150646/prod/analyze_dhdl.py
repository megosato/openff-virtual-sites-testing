import os
import pickle
import matplotlib.pyplot as plt
import numpy as np
import math
def smooth(x, window_len=11, window='hanning'):
    if x.ndim != 1:
        raise ValueError("smooth only accepts 1 dimension arrays.")
    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than "
                         "window size.")
    if window_len < 3:
        return x
    if window not in ['flat', 'hanning', 'hamming',
                      'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', "
                         "'bartlett', 'blackman'")
    s = np.r_[2*x[0]-x[window_len:1:-1], x, 2*x[-1]-x[-1:-window_len:-1]]
    # moving average
    if window == 'flat':
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')
    y = np.convolve(w/w.sum(), s, mode='same')
    return y[window_len-1:-window_len+1]

protocols = ['vdw', 'bonded']
for p in protocols:

    max_y = -1000000000000

    
    smooth_dict = {}


    for index,l in enumerate(list(range(0,20))):
        xs,ys,dhdls,xs2 = [],[],[],[]
        file = os.path.join('%s'%(p), 'dhdl_%s.pickle'%l)

        a = open(file, 'rb')
        dhdl = pickle.load(a)
        y = smooth(np.array(dhdl),window_len=100)

        a.close()

        max_y_window = max(y)

        if max_y_window > max_y:
            max_y = max_y_window

        smooth_dict[index] = y


    fig, ax = plt.subplots(4,5, figsize=(25, 20))
    for index,l in enumerate(list(range(0,20))):
        lam = l
        xs,ys,dhdls,xs2 = [],[],[],[]
        x = [i/5000 for i in list(range(0,len(dhdl)))]

        dhdl = smooth_dict[index]


        ax.flatten()[index].plot(x, smooth(np.array(dhdl),window_len=100),'-o', alpha=0.4,markersize=1)
        ax.flatten()[index].set_ylim([0,math.ceil(max_y / 10) * 10])
        ax.flatten()[index].set_title('%s lambda %i'%(p,l))
        ax.flatten()[index].set_ylabel('dH/dl')
        ax.flatten()[index].set_xlabel('simulation time in ns')
    plt.legend()
    plt.show()
    plt.savefig('%s.png'%(p))
