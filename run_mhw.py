import numpy as np
from datetime import date
from matplotlib import pyplot as plt
import pandas as pd
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


def generate_random_sst():
    start_date = "2025-01-10"
    end_date = "2025-03-31"
    sst_min = 20.0
    sst_max = 30.0

    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    sst_values = np.random.uniform(sst_min, sst_max, len(date_range))

    df = pd.DataFrame({
        "Date": date_range,
        "SST": sst_values
    })
    return df

sst_to_predict = generate_random_sst()

t_predict = pd.Series(sst_to_predict.Date).apply(lambda x: x.toordinal())
sst_predict = sst_to_predict.SST

# mhws, clim = mhw.detect(t_predict, sst_predict, climatologyPeriod=[2025, 2025], alternateClimatology=[t, sst])


mhws, clim = mhw.detect(t, sst)


plt.figure(figsize=(14,10))
plt.subplot(2,1,1)
# Plot SST, seasonal cycle, and threshold
plt.plot(dates, sst, 'k-')
plt.plot(dates, clim['thresh'], 'g-')
plt.plot(dates, clim['seas'], 'b-')
plt.title('SST (black), seasonal climatology (blue), \
          threshold (green), detected MHW events (shading)')
plt.xlim(dates[0], dates[-1])
plt.ylim(sst.min()-0.5, sst.max()+0.5)
plt.ylabel(r'SST [$^\circ$C]')

plt.show()


