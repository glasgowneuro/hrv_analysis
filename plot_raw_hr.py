import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import datetime
from datetime import datetime
import sys

if (len(sys.argv)<3):
    print("Usage: {} rawfile hrfile".format(sys.argv[0]))
    exit(1)

raw = np.loadtxt(sys.argv[1])
hr = np.loadtxt(sys.argv[2])

fig = plt.figure()
ax1 = plt.subplot(311)
ax1.set_title('ECG')
plt.plot(raw[:,0],raw[:,1])
ax2 = plt.subplot(312, sharex = ax1)
ax2.set_title('EEG')
plt.plot(raw[:,0],raw[:,2])
ax3 = plt.subplot(313, sharex = ax1)
ax3.set_title('HR')
plt.plot(hr[:,0],hr[:,1])


plt.show()
