"""
Written by Erlend L. Gundersen
    erlend.l.gundersen@gmail.com


NOTE 1: Before running, enter a path (line 15 in this script).
NOTE 2: The "Tools" folder is required to be in the same directory as main.py
NOTE 3: Follow the instructions in the command window.
NOTE 4: Plots may open as a seperate window in the background.
NOTE 5: See README.txt for information about libraries, variables, parameters, etc.
"""

#%% SETUP AND IMPORT

print("ENTER A PATH IN THE SCRIPT BEFORE RUNNING!")
# Enter the path to a folder with zip files containing dicom files (e.g. !!DICOM)
path = "C:/Users/Erlend/Desktop/!!DICOM/" # ENTER PATH HERE!

import numpy as np
import sys

# Giving access to the "Tools" folder
sys.path.insert(0, './Tools')

import dcm_tools
import display_tools
import segmentation_tools


#%% LOADING

# Selecting a dicom series from a folder of zip files
# output: dicoms: list of dicom objects
#  input: path: path to folder of zips with dicoms
#  input: unzip = True/False (unzip or not)
#  input: preview = True/False (preview collages of all series in folder or not)
dicoms = dcm_tools.dicoms_from_path_of_zips(path, unzip=False, preview=False)

# Convert list of dicoms to 3D volume (using interpolation)
# output: volume: 3D array of pixel values (X, Y, Z)
#  input: dicoms: list of dicom objects (a series of sorted slices)
volume = dcm_tools.get_volume(dicoms)

# Invert first dimension (X=0) if the model is upside-down
volume = np.flip(volume,0)

#%% CLUSTERING

# Select an amount of clusters
k = int(input("Select an amount of clusters: "))
# k = 6

#%% K-Means Clustering

# labels:  3D array of which center each pixel value belongs to
# centers: centers in the clustering (k grayscale values)
labels, centers = segmentation_tools.k_means(volume, k=k)

# 4D array of pixel values from each cluster (cluster, X, Y, Z)
clusters_k_means = segmentation_tools.get_clusters(labels, centers)

#%% Fuzzy Clustering (FCM) (VERY SLOW)
fuzzy_choice = input("Fuzzy clustering is slow. Do you want to run it? (y/n): ")

if fuzzy_choice == "y":

    # labels:  3D array of which center each pixel value belongs to
    # centers: centers in the clustering (k grayscale values)
    labels, centers = segmentation_tools.FCM(volume, k=k)

    # 4D array of pixel values from each cluster (cluster, X, Y, Z)
    clusters_FCM = segmentation_tools.get_clusters(labels, centers)

#%% Select k-means or fuzzy clustering before plotting
if fuzzy_choice == "y":
    method_choice = input("Choose result to display (k-means/fuzzy): ")
    if method_choice == "k-means":
        clusters = clusters_k_means # MUCH FASTER
    elif method_choice == "fuzzy":
        clusters = clusters_FCM    # MUCH SLOWER
else:
    clusters = clusters_k_means

#%% SHOW CLUSTERS

# mode:    isosurface (only render surfaces) or volume (render a solid volume)
# opacity: None, a number, "linear", "sigmoid", ... (see pyvista documentation)
# denoise: Gaussian smoothing with sigma 0.5 for each cluster (True/False)
# largest: show only the largest connected part of the cluster (True/False)
#          (largest does not support volume mode yet)

# colors of the plots are set from "cmap" in the functions in segmentation_tools

# A few examples are listed below.
# For show_individual_clusters select clusters in the command window

#%% Show all clusters (EXAMPLE 1.1)
segmentation_tools.show_all_clusters(clusters,
                                mode="isosurface",
                                opacity=0.25,
                                denoise=True,
                                largest=False)

#%% Show all clusters (EXAMPLE 1.2)
segmentation_tools.show_all_clusters(clusters,
                                mode="isosurface",
                                opacity=None,
                                denoise=True,
                                largest=True)

#%% Show all clusters (EXAMPLE 1.3)
segmentation_tools.show_all_clusters(clusters,
                                mode="volume",
                                opacity="linear",
                                denoise=False,
                                largest=False)

#%% Show individual clusters (EXAMPLE 2.1)
segmentation_tools.show_individual_clusters(clusters,
                                       mode="isosurface",
                                       opacity=None,
                                       denoise=True,
                                       largest=True)

#%% Show individual clusters (EXAMPLE 2.2)
segmentation_tools.show_individual_clusters(clusters,
                                       mode="isosurface",
                                       opacity=0.9,
                                       denoise=True,
                                       largest=True)

#%% Show individual clusters (EXAMPLE 2.3)
segmentation_tools.show_individual_clusters(clusters,
                                       mode="volume",
                                       opacity="linear",
                                       denoise=True,
                                       largest=True)

#%% SAVE CLUSTERS AS STL FILES (CREATES FOLDER(S) AUTOMATICALLY IN CURRENT DIRECTORY)

# The user may select the desired file type in the argument of save_all_3d

if input("Do you want to export the clusters as .stl files? (y/n): ") == "y":
    # Save all clusters from K-Means
    segmentation_tools.save_all_3d(clusters_k_means,
                                   folder_name="3D Objects K-Means",
                                   file_type=".stl",
                                   series_number=dicoms[0].SeriesNumber,
                                   denoise=True,
                                   largest=True)

    # Save all clusters from FCM
    if fuzzy_choice == "y":
        segmentation_tools.save_all_3d(clusters_FCM,
                                       folder_name="3D Objects FCM",
                                       file_type=".stl",
                                       series_number=dicoms[0].SeriesNumber,
                                       denoise=True,
                                       largest=True)

#%% THRESHOLDING

# The user may use sliders to select upper and lower thresholding limit. This
# may be used for segmentation of different organs based on pixel/grayscale values.

# opacity: None, a number, "linear", "sigmoid", ... (see pyvista documentation)
# denoise: Gaussian smoothing with sigma 0.5 for each cluster (True/False)
# largest: show only the largest connected part of the cluster (True/False)
#          (largest does not support volume mode yet)

# Two examples are listed below.

#%% Threshold with sliders (EXAMPLE 3.1)
segmentation_tools.threshold_sliders(volume,
                                opacity="linear",
                                denoise=True,
                                largest=False)

#%% Theshold with sliders (EXAMPLE 3.2)
segmentation_tools.threshold_sliders(volume,
                                opacity=None,
                                denoise=True,
                                largest=True)

#%% OTHER FUNCTIONALITIES

# The "Testing" folder also contains a few additional funcitonalities such as
# converting dicom files to image files, edge detection, header manipulation, etc.

#%% Axial, coronal and sagital

# Displaying the dicom series from three different angles (axial, coronal and sagital)
display_tools.show_axial_coronal_sagital(dicoms)

#%% Histogram

# See the frequency of each pixel value. Useful when thresholding.
display_tools.show_histogram(volume, bins=100, log=True)

#%% Header

# Information from the first dicom file in the series
print(dicoms[0])

#%% Slideshow

# Displaying all the slides of the series one by one
display_tools.show_all(dcm_tools.get_pixels(dicoms))

