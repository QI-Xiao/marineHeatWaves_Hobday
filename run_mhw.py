import numpy as np
from datetime import date
from matplotlib import pyplot as plt
import marineHeatWaves as mhw


# Generate time vector using datetime format (January 1 of year 1 is day 1)
t = np.arange(date(1982,1,1).toordinal(),date(2014,12,31).toordinal()+1)
dates = [date.fromordinal(tt.astype(int)) for tt in t]
# Generate synthetic temperature time series
sst = np.zeros(len(t))
sst[0] = 0 # Initial condition
a = 0.85 # autoregressive parameter
for i in range(1,len(t)):
    sst[i] = a*sst[i-1] + 0.75*np.random.randn() + 0.5*np.cos(t[i]*2*np.pi/365.25)
sst = sst - sst.min() + 5.


plt.figure(figsize=(10, 5))
plt.plot(dates, sst, label='Synthetic Temperature')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.title('Synthetic Sea Surface Temperature Time Series')
plt.grid(True)
plt.legend()
plt.show()

mhws, clim = mhw.detect(t, sst)
