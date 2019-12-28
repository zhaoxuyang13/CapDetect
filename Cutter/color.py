# import the necessary packages
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
# color detect using mainly K-Clustering
# reference https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/

# input clt, return percentages
def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)
    # normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
	# return the histogram
	return hist
'''
# not used function to plot color percentage
def plot_colors(hist, centroids):
# initialize the bar chart representing the relative frequency
	# of each of the colors
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0
 
	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
			color.astype("uint8").tolist(), -1)
		startX = endX
	
	# return the bar chart
	return bar
'''
import webcolors

def closest_colour_name(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour_name(requested_colour)
        actual_name = None
    return actual_name, closest_name


def detect_color(images):
	colorlist = []
	for img in images:
		image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		image = image.reshape((image.shape[0] * image.shape[1], 3))
		clt = KMeans(n_clusters = 2)
		clt.fit(image)
		hist = centroid_histogram(clt)
		if hist[0] > hist[1] :
			prominant_color = clt.cluster_centers_[0]
		else :
			prominant_color = clt.cluster_centers_[1]
		closestColor = closest_colour_name(prominant_color)
		colorlist.append(webcolors.name_to_rgb(closestColor))
        # colorlist.append(prominant_color.astype("uint8"))
	return colorlist
