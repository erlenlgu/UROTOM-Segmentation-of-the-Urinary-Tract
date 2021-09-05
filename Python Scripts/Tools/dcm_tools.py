"""
Written by Erlend L. Gundersen
    erlend.l.gundersen@gmail.com
"""

import numpy as np
import pydicom as dicom
import scipy.ndimage as nd

import file_tools
import display_tools


# Input:  file_paths: list of paths (as strings) to dicom files
# Output: array of dicom objects
def get_array(file_paths):
    return np.array([dicom.dcmread(i) for i in file_paths])


# Input:  dicom_objects: array of dicom objects
# Output: 3D array of pixel values for each dicom object (object, pixel, pixel)
def get_pixels(dicoms):
    return np.array([dcm.pixel_array for dcm in dicoms])


# Sorting list of dicom objects by series number and saving each series in an
# own tag in a dictionary as dicom objects
def series_sort(dicoms):
    dic = {} # empty dictionary
    for dcm in dicoms:
        # if SeriesNumber is not already in the dictionary it creates a new tag
        # it also appends the dicom object to the tag of the corresponding series
        dic.setdefault(dcm.SeriesNumber, []).append(dcm)
    return dic


# Arranging the dicom series in a 3D array
# Interpolating in three dimensions to get equal spacing on each axis
# input: dicoms: array of dicom objects
# output: pixel values (slice, X, Y)
def get_pixels_reshaped(dicoms):
    print("\tReshaping...")

    # If the input is a list of dicom objects
    if np.shape(dicoms) != ():
        # Getting pixel values from the dicoms objects
        slices = get_pixels(dicoms)
        
        # Defining spacing between pixels in 3D
        spacing = np.array([dicoms[0].SliceThickness,
                            dicoms[0].PixelSpacing[0],
                            dicoms[0].PixelSpacing[1]])
        
    # If the input is a single dicom object
    else:
        # Getting pixel values from the dicom object
        slices = dicoms.pixel_array
        
        # Defining spacing between pixels in 2D
        spacing = np.array([dicoms.PixelSpacing[0],
                            dicoms.PixelSpacing[1]])

    return nd.interpolation.zoom(slices, spacing)


# Input:  dicoms: list of dicom objects (one series)
# Output: volume: 3D Array of pixel values (X, Y, Z)
def get_volume(dicoms):
    print("Creating volume...")

    # Printing original shape of the 3D array
    print("\tOriginal shape:  ("+str(len(dicoms))+", " +
          str(dicoms[0].Rows)+", "+str(dicoms[0].Columns)+")")

    # Interpolating between slices and correcting scaling on axis
    slices = get_pixels_reshaped(dicoms)

    # Printing new shape of the 3D array
    print("\tAfter reshaping:", np.shape(slices))

    # Creating an empty volume with the correct dimensions
    img_shape = list(slices[0].shape)
    img_shape.append(len(slices))
    volume = np.zeros(img_shape)

    # Combining 2D slices to 3D array
    for i, array2D in enumerate(slices):
        volume[:, :, i] = array2D  # Format (X, Y, Z)

    return volume


# Selecting a dicom series from a folder of zip files
# output: dicoms: list of dicom objects
#  input: path: path to folder of zips with dicoms
#  input: unzip = True/False (unzip or not)
#  input: preview = True/False (preview collages of all series in folder or not)
def dicoms_from_path_of_zips(folder_path, unzip=False, preview=False):
    # Run if unzipping in needed
    if unzip:
        print("Unzipping...")
        file_tools.zip_extract_all(folder_path)

    # Creating a dictionary of all paths to dicom files and their folders
    dic = file_tools.path_dic(folder_path)

    # Select folder
    print("\nFolders found:\n", dic["folder_names"],
          "\nFolder numbers:\n", dic["folder_numbers"])
    
    # Choose which folder to display
    folder_number = int(input("Select a folder number: "))

    # Previewing series in the specified folder
    if preview:
        print("\nPreviewing all series in " +
              dic["folder_names"][folder_number]+"...")
        display_tools.show_everything_in_folder(folder_path, folder_number, stop=16)

    # Detecting series in folder
    folder = get_array(dic["file_paths"][folder_number])
    folder_sorted = series_sort(folder)

    # Select series
    print("\nSeries found:\n", [int(i) for i in folder_sorted.keys()])
    series_number = int(input("Select a series: "))
    print(" ")

    # Selected series from the selected folder
    return folder_sorted[series_number]
