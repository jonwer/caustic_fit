#Version 2 of Code for Caustic Fit
#Jonathan Werger

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd

plt.rcParams['font.size'] = 8.0
plt.rcParams['figure.dpi'] = 300

#parameters to change
wavelength = 1030   #in nm
diameter = True    #if data is diameter of beam, set to true; if it is radius, set to false
weighted_fit = True    #weighs points around center more for more accurate fit
#Weighting is proportional to inverse of beam size, i.e. errors in measurement grow proportional with beam size

#data should have three rows: distance z, beam size in x, beam size in y
#beam size should be radius or diameter of 1/e² beam size
d = pd.read_csv('data.csv',sep=';',decimal=",")
df = d.values
z=df[:,0]
wx=df[:,1]/2
wy=df[:,2]/2

#caustic function to be fitted to data
def Caustic(z, M2, w0, z0):
    w = np.sqrt((w0)**2 + M2**2 * (wavelength/(np.pi*w0))**2 * (z-z0)**2)
    return w

#guess starting parameters
guess_z0x = z[np.argmin(wx)]
guess_z0y = z[np.argmin(wy)]
guess_M2x = 5
guess_M2y = 5
guess_w0x = wx.min()
guess_w0y = wy.min()

#curve fit on x and y
if weighted_fit==True:
    parameters, covariance = curve_fit(Caustic, z, wx, p0=[guess_M2x,guess_w0x,guess_z0x], sigma=wx, maxfev=5000)
    [fit_M2x,fit_w0x,fit_z0x] = parameters
    parameters, covariance = curve_fit(Caustic, z, wy, p0=[guess_M2y,guess_w0y,guess_z0y], sigma=wy, maxfev=5000)
    [fit_M2y,fit_w0y,fit_z0y] = parameters
else:
    parameters, covariance = curve_fit(Caustic, z, wx, p0=[guess_M2x,guess_w0x,guess_z0x], maxfev=5000)
    [fit_M2x,fit_w0x,fit_z0x] = parameters
    parameters, covariance = curve_fit(Caustic, z, wy, p0=[guess_M2y,guess_w0y,guess_z0y], maxfev=5000)
    [fit_M2y,fit_w0y,fit_z0y] = parameters
    

fit_wx = Caustic(z, fit_M2x, fit_w0x, fit_z0x)
fit_wy = Caustic(z, fit_M2y, fit_w0y, fit_z0y)


#plot data points and fits
fig,ax = plt.subplots()

ax.plot(z, wx, 'o',color='C1', label='data_x')
ax.plot(z, fit_wx, '-',color='C1', label='fit_x')
ax.plot(z, wy, 'o',color='C2', label='data_y')
ax.plot(z, fit_wy, '-',color='C2', label='fit_x')

ax.legend()
plt.ylim(bottom=0)
#plt.xlim(-50,150)

#draws M²,focus radius and focus position in graph
text_in_plot = str("Gain:    x             y \nM²=    %.2f       %.2f \nw0=   %.1f      %.1f \nz0=    %.1f        %.1f" % (abs(fit_M2x),abs(fit_M2y),fit_w0x,fit_w0y,fit_z0x,fit_z0y))

plt.annotate(text_in_plot, xy=(0.38, 0.8), xycoords='axes fraction')

print('Gain:')
print("\t x \t\t y")
print("M²= %.2f \t %.2f" %(abs(fit_M2x),abs(fit_M2y)))
print("w0= %.1f \t %.1f" %(fit_w0x,fit_w0y))
print("z0= %.1f \t %.1f" %(fit_z0x,fit_z0y))
print()