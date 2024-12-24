import os
import numpy as np
import matplotlib.pyplot as plt

def single_file_fft(file_name, n_channel):
	data = np.loadtxt(file_name)
	if (len(data) % n_channel != 0):
		print("Incorrect channel number!")
		exit()

	# a list for channel1, channel2, ..., channeln
	channels = []
	for i in range(n_channel):
		channels.append(np.zeros(int(len(data) / n_channel)))

	# store channel1, channel2 as channels[1], channels[2]
	for i in range(len(data)):
		channels[i % n_channel][int(i / n_channel)] = data[i]

	# do fft to n channels
	for i in range(n_channel):
		channels[i] = np.fft.fft(channels[i])

	# convert complex number to real number
	channels = np.abs(channels)
	
	# save channels_fft before return!
	save_name = file_name.split("/")[1] + "_" + file_name.split("/")[2] + "_fft.txt"

	f = open(save_name, "w")
	f.write("x		CH1		CH2		CH3\n")
	for i in range(len(channels[0])):
		f.write(str(i) + "		")
		for j in range(n_channel):
			f.write(str(channels[j][i]) + "		")
		f.write("\n")
	f.close()

	return channels

def fft_plot(file_name, channels, n_channel, modulation_freq, n_modulation):
	# list for modulation_freq to be marked in the axis
	x_mark = np.zeros(n_modulation)
	y_mark = np.zeros(n_modulation)

	# plot n channels
	plt.figure()
	for i in range(n_channel):
		# list for modulation_freq to be shown in the axis
		for j in range(n_modulation):
			x_mark[j] = (j+1) * modulation_freq
			y_mark[j] = channels[i][int(x_mark[j])]

		plt.subplot(n_channel, 1, i + 1)
		plt.plot(channels[i])
		plt.title("channel " + str(i + 1))

		# show the image in the domain of modulation_freq only
		x_mark_max = max(x_mark)
		y_mark_max = max(y_mark)
		x_mark_min = min(x_mark)
		y_mark_min = min(y_mark)
		plt.xlim(x_mark_min - x_mark_max/10, x_mark_max + x_mark_max/10)
		plt.ylim(y_mark_min - y_mark_max/10, y_mark_max + y_mark_max/10)

		# mark the modulation_freq
		if i == 0:
			# the graph of channel 1, reference
			# in this case, only one modulation_freq (w1) is considered!!
			plt.xticks(x_mark)
			plt.annotate("w" + str(1) + " = " + str(round(y_mark[0], 2)), (x_mark[0], y_mark[0]), color = "red")
		
		else:
			# for channel2, channel3, n_modulaton is considered!!
			for j in range(n_modulation):
				plt.xticks(x_mark)
				plt.annotate("w" + str(j+1) + " = " + str(round(y_mark[j], 2)), (x_mark[j], y_mark[j]), color = "red")

		# make top and right lines invisible
		ax = plt.gca()
		ax.spines["top"].set_color("none")
		ax.spines["right"].set_color("none")
		
	fig = plt.gcf()
	fig.set_size_inches(9, 9)
	fig.suptitle(file_name, color = "r")

	save_name = file_name.split("/")[1] + "_" + file_name.split("/")[2] + "_fft.png"
	plt.savefig(save_name, bbox_inches = "tight")
	plt.show()


# --------------------------variables can be modify--------------------------


file_name = "sic-gold-intensity dep-10-08-2024/5000uw/0.000000"
n_channel = 3
modulation_freq = 1000
n_modulation = 4


# ---------------------------------------------------------------------------


channels_fft = single_file_fft(file_name, n_channel)
fft_plot(file_name, channels_fft, n_channel, modulation_freq, n_modulation)

