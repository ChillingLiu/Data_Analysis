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

	return channels



def single_folder_fft(folder_name, n_channel):
	# manipulate with the files in the folder, remove Auto_correlation.txt, sort the files by name
	files = os.listdir(folder_name)
	files.remove("Auto_correlation_data.txt")
	files.sort(key=lambda x:int(x.split('.')[0]))
		
	data = np.loadtxt(folder_name + "/" + files[0])
	if (len(data) % n_channel != 0):
		print("Incorrect channel number!")
		exit()

	# a list for channel1, channel2, ..., channeln
	# the output from single_file_fft() is the type of complex numbers
	channels_average = np.zeros((n_channel, int(len(data) / n_channel)))

	# for every file in the folder, do single_file_fft, and sum them together to get the average.
	for i in range(len(files)):
		file_name = folder_name + "/" + files[i]
		channels_average += single_file_fft(file_name, n_channel)
	
	channels_average = np.divide(channels_average, len(files))
	return channels_average


# You MUST let all folders have the same suffix, like "70uw", "100uw"!
def all_folders_fft(data_folder_name, folder_start_index, folder_end_index, n_channel, modulation_freq, n_modulation):
	folders_all = os.listdir(data_folder_name)
	folders_all.sort(key=lambda x:int(x.split('uw')[0]))

	# need a new list to store the folders_name in the range
	folders_in_range = []
	for i in range(len(folders_all)):
		if int(folders_all[i].split('uw')[0]) >= folder_start_index and int(folders_all[i].split('uw')[0]) <= folder_end_index:
			folders_in_range.append(folders_all[i])

	files = os.listdir(data_folder_name + "/" + folders_in_range[0])
	files.remove("Auto_correlation_data.txt")

	data = np.loadtxt(data_folder_name + "/" + folders_in_range[0] + "/" + files[0])
	if (len(data) % n_channel != 0):
		print("Incorrect channel number!")
		exit()

	# a 3D matrix to store every average data from every single folder
	channels_average_all = np.zeros((len(folders_in_range), n_channel, int(len(data) / n_channel)))

	# for every folder in the folder, do single_folder_fft, and store them.
	for i in range(len(folders_in_range)):
		folder_name = data_folder_name + "/" + folders_in_range[i]
		channels_average_all[i] = single_folder_fft(folder_name, n_channel)
		print("Finish: " + folder_name)
	
	# store the modulation_freq for every folder, list[0][0] means w1 for channel 1, list[1][1] means w2 for channel 2, ...
	modulation_freq_list = np.zeros((n_channel, n_modulation, len(folders_in_range)))
	for i in range(n_channel):
		for j in range(n_modulation):
			for k in range(len(folders_in_range)):
				modulation_freq_list[i][j][k] = channels_average_all[k][i][(j+1) * modulation_freq]
	
	# save modulation_freq_list before return!
	save_name = "modulation_freq(" + str(folder_start_index) + ", " + str(folder_end_index) + ")_fft.txt"

	f = open(save_name, "w")
	f.write("x		Ref		w1		w2		w3		w4		f1		f2		f3		f4\n")
	for i in range(len(folders_in_range)):
		f.write(folders_in_range[i].split('uw')[0] + "		")
		f.write(str(modulation_freq_list[0][0][i]) + "		")
		for j in range(1, n_channel):
			for k in range(n_modulation):
				f.write(str(modulation_freq_list[j][k][i]) + "		")
		f.write("\n")
	f.close()

	return modulation_freq_list



def modulation_freq_plot(data_folder_name, folder_start_index, folder_end_index, modulation_freq_list, n_channel, n_modulation, plot_log):
	# prepare x axis
	folders_all = os.listdir(data_folder_name)
	folders_all.sort(key=lambda x:int(x.split('uw')[0]))
	# need a new list to store the folders_name in the range
	folders_in_range = []
	for i in range(len(folders_all)):
		if int(folders_all[i].split('uw')[0]) >= folder_start_index and int(folders_all[i].split('uw')[0]) <= folder_end_index:
			folders_in_range.append(folders_all[i])

	# colors and markers to indicate the modulation_freq, up to n_modulation = 8
	colors = ["red", "orange", "green", "blue", "purple", "pink", "cyan",   "brown"]
	markers = [".", "^", "o", "s", "p", "h", "*", ","]

	n_modulation_tmp = n_modulation

	# plot w1, w2, w3, ... wn for n channels!
	for i in range(n_channel):
		# to deal with the channel 1, reference with only 1 modulation frequency
		if i == 0:
			n_modulation = 1
		else:
			n_modulation = n_modulation_tmp

		# prepare plot information
		x_axis = []
		for j in range(len(folders_in_range)):
			x_axis.append(folders_in_range[j].split('uw')[0])

		x_plot = np.zeros(len(x_axis))
		for j in range(len(x_plot)):
			x_plot[j] = int(x_axis[j])

		# prepare x for polynomial fit
		x_poly = np.linspace(x_plot[0], x_plot[len(x_plot)-1], 1000)

		plt.subplot(n_channel, 1, i + 1)

		if plot_log == True:
			x_plot = np.log10(x_plot)
			x_poly = np.linspace(x_plot[0], x_plot[len(x_plot)-1], 1000)
			for j in range(n_modulation):
				plt.plot(x_plot, np.log10(modulation_freq_list[i][j]), linestyle = " ", marker = markers[j], color = colors[j])
				
				# polyfit to draw the line
				z = np.polyfit(x_plot, np.log10(modulation_freq_list[i][j]), 1)
				p = np.poly1d(z)
				fx = p(x_poly)
				p = np.poly1d(np.round(z, 3))
				plt.plot(x_poly, fx, color = colors[j], label = "w" + str(j) + ": " + str(p))

			for k in range(len(x_axis)):
				x_axis[k] = str(round(x_plot[k], 2))
			plt.xticks(x_plot, x_axis)
		else:
			for j in range(n_modulation):
				plt.plot(x_plot, modulation_freq_list[i][j], linestyle = " ", marker = markers[j], color = colors[j])

				# polyfit to draw the line
				z = np.polyfit(x_plot, modulation_freq_list[i][j], 2)
				p = np.poly1d(z)
				fx = p(x_poly)
				p = np.poly1d(np.round(z, 3))
				plt.plot(x_poly, fx, color = colors[j], label = "w" + str(j) + ": " + str(p))
			plt.xticks(x_plot, x_axis, rotation = 60)

		plt.legend(loc = "upper left")
		plt.title("channel " + str(i + 1))

		# make top and right lines invisible
		ax = plt.gca()
		ax.spines["top"].set_color("none")
		ax.spines["right"].set_color("none")		

	fig = plt.gcf()
	fig.set_size_inches(9, 9)


# --------------------------variables can be modify--------------------------

data_folder_name = "sic-gold-intensity dep-10-08-2024"
n_channel = 3
modulation_freq = 1000
n_modulation = 4

# if you want the average of data from all folders, we will assume to take all files in a folder,
# this case, we don't need "files_start_index", and "files_end_index" anymore!

folder_start_index = 70
folder_end_index = 5000

# ---------------------------------------------------------------------------


modulation_freq_list = all_folders_fft(data_folder_name, folder_start_index, folder_end_index, n_channel, modulation_freq, n_modulation)

#whether to plot the modulation_freq as the form log10
plot_log = False
plt.figure()
modulation_freq_plot(data_folder_name, folder_start_index, folder_end_index, modulation_freq_list, n_channel, n_modulation, plot_log)
plt.savefig("modulation_freq(" + str(folder_start_index) + ", " + str(folder_end_index) + ")_fft.png", bbox_inches = "tight")
plt.show()

plot_log = True
plt.figure()
modulation_freq_plot(data_folder_name, folder_start_index, folder_end_index, modulation_freq_list, n_channel, n_modulation, plot_log)
plt.savefig("modulation_freq(" + str(folder_start_index) + ", " + str(folder_end_index) + ")_fft_log10.png", bbox_inches = "tight")
plt.show()
