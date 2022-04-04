import numpy as np
import cv2
import sys

# Giving access to the Tools folder
sys.path.insert(0, '../Tools')

import display_tools
import dcm_tools
import segmentation_tools
import file_tools

# Enter path of folder with zip files
path = "C:/Users/Erlend/Desktop/!!DICOM/"

# Enter path where converted images should be saved
# (A folder will be generated.)
save_path = "C:/Users/Erlend/Desktop/"

print("ENTER PATHS IN SCRIPT BEFORE RUNNING!\n")

# Run if unzipping in needed
file_tools.zip_extract_all(path)

# Creating a dictionary of all paths to dicom files and their folders
from path_tools import path_dic
dic = path_dic(path)

#%% The number selects which folder to print from
print("Folders:\n",dic["folder_names"],"=",dic["folder_numbers"]) 
folder_number = int(input("Select a folder number: ")) # Choose which folder to display
   
#%% Plotting all series in the specified folder
print("\nPlotting previews of all series in "+dic["folder_names"][folder_number])
display_tools.show_everything_in_folder(path, folder_number, stop=16)
  
#%% Sorting and Loading Folder Contents
dicoms_folder = dcm_tools.get_array(dic["file_paths"][folder_number]) # Selecting the first folder
dicoms_folder_sorted = dcm_tools.series_sort(dicoms_folder) # Sorting folder by series

print("\nSeries: "+str(dicoms_folder_sorted.keys()))
series_number = int(input("Select a series number: ")) # Choose series

# List of dicom files in one series
dicoms_series = dicoms_folder_sorted[series_number] # Selecting Series

# Array of pixels from one series
pixels_series = dcm_tools.get_pixels(dicoms_series)

#%% Histogram of pixel values for one image in series
#show_histogram(dicoms_series[0].pixel_array)

#%% Thresholding

# Getting thresholded pixels from array of dicom files
def threshold(dicom_files, l=950, u=1050):
    dicom_pixels_thresholded = []
    for dicom_file in dicom_files:
        _,thr = cv2.threshold(dicom_file.pixel_array,l,u,cv2.THRESH_BINARY)
        dicom_pixels_thresholded.append(thr)
    return np.array(dicom_pixels_thresholded)

pixels_series_thr = threshold(dicoms_series)

#%% K-Means Clustering Segmentation
pixels_series_k_means = np.array([segmentation_tools.k_means(i)[0] for i in pixels_series])

#%% Fuzzy Clustering Segmentation (not supported...)
#pixels_series_FCM = np.array([segmentation_tools.FCM(i)[0] for i in pixels_series])

#%% Slideshows
display_tools.show_all(dcm_tools.get_pixels(dicoms_series))
display_tools.show_all(pixels_series_thr)
display_tools.show_all(pixels_series_k_means)
#show_all(pixels_series_FCM)

#%% Axial Coronal Sagital
display_tools.show_axial_coronal_sagital(dicoms_series)

#%% Collages
display_tools.show_collage(pixels_series)
display_tools.show_collage(pixels_series_thr)
display_tools.show_collage(pixels_series_k_means)
#display_tools.show_collage(pixels_series_FCM)
