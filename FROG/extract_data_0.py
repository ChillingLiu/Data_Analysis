import glob
import re
import numpy as np
import matplotlib.pyplot as plt

DataName = "chosen_0_center.txt"
WavelengthName = "wavelength_chosen_0_center.txt"
TimeDelayName = "time_delay_chosen_0_center.txt"

ImageName = "chosen_0.png"

# read data
directory = "/home/xiaoqi/Desktop/frog/shg/0/"
files = glob.glob(directory + '*.txt')

tmp = np.loadtxt(directory + "0_S1_1_.txt")
wavelength = tmp[:,0]
dataz = np.zeros((len(wavelength),len(files)))   ##density 2-D data
for i in range(1, len(files) + 1):
	filename = directory + "0_S1_" + str(i) + "_.txt"
	data = np.loadtxt(filename)
	intensity = data[:, 1]
	for j in range(0, len(intensity)):
		dataz[j, i - 1] = intensity[j]
print('ok')

# store data of the original frog trace of a single period
minx_period = 273
maxx_period = 1070
lenx_period = maxx_period - minx_period
miny_period = 0
maxy_period = 748
f = open("tmp.txt", "w")
for i in range(miny_period, maxy_period):
	for j in range(minx_period, maxx_period):
		f.write(str(dataz[i][j]) + " ")
	f.write("\n")
f.close()

wavelength_square = []
for i in range(miny_period, maxy_period):
	wavelength_square.append(wavelength[i])

# change indexes of time_delay to converted_time_delay and store it again.
time_delay = np.arange(0, lenx_period)/lenx_period
converted_time_delay = 1/np.pi * (np.arcsin(2*time_delay - 1) + np.pi/2)

shift = np.arange(lenx_period - minx_period, lenx_period)/lenx_period
converted_shift = 1/np.pi * (np.arcsin(2*time_delay - 1) + np.pi/2)
shift_distance = np.max(converted_shift) - np.min(converted_shift)

converted_time_delay = (converted_time_delay + shift_distance) * lenx_period * 0.1
time_delay = (time_delay * lenx_period + minx_period) * 0.1

"""
time_delay = np.arange(0, len(files))/len(files)
converted_time_delay = 1/2 * (np.sin(time_delay * np.pi - np.pi/2) + 1)
#converted_time_delay = 1/np.pi * (np.arcsin(2*time_delay - 1) + np.pi/2)
converted_time_delay = converted_time_delay * len(files) * 0.1
time_delay = time_delay * len(files) * 0.1
"""


# store data again, because the previous one is not square!
len_chosen = 500
#center = int((minx_period + maxx_period)/2)
center = 710 # If you want specific position of the center.
# Be careful to pick to center while making sure maxx_chosen < maxx_period

minx_chosen = int(center - len_chosen/2)
maxx_chosen = int(center + len_chosen/2)
miny_chosen = int(748/2 - len_chosen/2)
maxy_chosen = int(748/2 + len_chosen/2)

f = open(DataName, "w")
for i in range(miny_chosen, maxy_chosen):
	for j in range(minx_chosen, maxx_chosen):
		f.write(str(dataz[i][j]) + " ")
	f.write("\n")
f.close()

testy = []
testx = []
f = open(WavelengthName, "w")
for i in range(miny_chosen, maxy_chosen):
	testy.append(wavelength_square[i])
	f.write(str(wavelength_square[i]) + "\n")
f.close()
f = open(TimeDelayName, "w")
for i in range(minx_chosen - minx_period, maxx_chosen - minx_period):
	testx.append(converted_time_delay[i])
	f.write(str(converted_time_delay[i]) + "\n")
f.close()


# plot
plt.figure()
plt.subplot(221)
im = plt.contourf(np.arange(0, len(files)/10, 0.1), wavelength, dataz, 20, cmap='jet')
plt.colorbar(im)
plt.xlabel('time delay (fs)')
plt.ylabel('Wavelength (nm)')
plt.title('Original FROG trace')
"""
plt.subplot(222)
im = plt.contourf(converted_time_delay, wavelength, dataz, 20, cmap='jet')
plt.colorbar(im)
plt.xlabel('time delay (fs)')
plt.ylabel('Wavelength (nm)')
plt.title('FROG trace with converted time delay')
"""
plt.subplot(222)
dataz2 = np.loadtxt("tmp.txt")
im = plt.contourf(time_delay, wavelength_square, dataz2, 20, cmap='jet')
plt.colorbar(im)
plt.xlabel('time delay (fs)')
plt.ylabel('Wavelength (nm)')
plt.title('Chosen FROG trace did not convert time delay')
"""
plt.subplot(223)
plt.plot(time_delay, time_delay, color = "blue", label = "time delay")
plt.plot(time_delay, converted_time_delay, color = "r", label = "converted time delay")
plt.legend(loc = 0)
"""
plt.subplot(223)
im = plt.contourf(converted_time_delay, wavelength_square, dataz2, 20, cmap='jet')
plt.colorbar(im)
plt.xlabel(str(len(converted_time_delay)) + ' time delay (fs)')
plt.ylabel(str(len(wavelength_square)) + ' wavelength (nm)')
plt.title('Chosen FROG Trace converted time delay')

plt.subplot(224)
testz = np.loadtxt(DataName)
im = plt.contourf(testx, testy, testz, 20, cmap='jet')
plt.colorbar(im)
plt.xlabel(str(len(testx)) + ' time delay (fs)')
plt.ylabel(str(len(testy)) + ' wavelength (nm)')
plt.title('Final Chosen FROG Trace converted time delay')

fig = plt.gcf()
fig.set_size_inches(11, 7)
fig.suptitle(ImageName, color = "r")
plt.savefig(ImageName, bbox_inches = "tight")

plt.show()
