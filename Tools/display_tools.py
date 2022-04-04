"""
Written by Erlend L. Gundersen
    erlend.l.gundersen@gmail.com
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid

import file_tools
import dcm_tools


# Showing a collage of images from array of 2D images
def show_collage(pixels,fig_num = 1):
    # Make a square grid
    num = pixels.shape[0]
    rows = int(np.ceil(np.sqrt(float(num))))

    fig = plt.figure(fig_num, [10, 10])
    
    # Adding title
    plt.rcParams.update({'font.size': 30}) # Increase font size
    plt.title(str(fig_num)), plt.axis("off") # title
    
    # Creating a grid
    grid = ImageGrid(fig, 111, nrows_ncols=[rows, rows])

    # Assigning images to different parts of the grid
    for i in range(num):
        grid[i].axis('off')
        grid[i].imshow(pixels[i])

    # Turn any unused axes off
    for j in range(i, len(grid)):
        grid[j].axis('off')
    
    plt.show()
    
     
# Showing a slideshow of images from array of 2D images
def show_all(images):
    for image in images:
        plt.imshow(image), plt.axis("off")
        plt.show()
        
        
# Showing a histogram of an array of pixels
def show_histogram(array, bins = 100, log=False): 
    plt.rcParams.update({'font.size': 22}) # Increase font size
    plt.hist(array.flatten(), bins), plt.title("Histogram")
    if log:
        plt.yscale("log") # logarithmic second axis
    plt.xlabel("Pixel Value"), plt.ylabel("Frequency")
    plt.show()
    
    
# Displaying all dicom images in a given folder
def show_everything_in_folder(path = ".", folder_number = 0, stop = 999, unzip = False):
    if unzip:
        file_tools.zip_extract_all(path)
        
    dic = file_tools.path_dic(path)
    for paths in dic["file_paths"][folder_number:folder_number+1]:
        print("Folder: "+dic["folder_names"][folder_number])
       
        dicoms = dcm_tools.get_array(paths)
        dicoms_sorted = dcm_tools.series_sort(dicoms) #remove "Numpy"
        for SeriesNumber in dicoms_sorted:
            print("\tSeries: "+str(SeriesNumber))
            show_collage(dcm_tools.get_pixels(dicoms_sorted[SeriesNumber][0:stop]), SeriesNumber)


# Showing axial, coronal and sagital view from array of dicom objects
def show_axial_coronal_sagital(dicoms):
    plt.rcParams.update({'font.size': 8}) # Increase font size
    
    # Sorting the slices
    slices = sorted(dicoms,key=lambda x:x.ImagePositionPatient[2])
    
    # Voxel Size: Pixel Spacing and Slice Thickness (using first file as reference)
    pixel_spacing = slices[0].PixelSpacing
    slices_thickess = slices[0].SliceThickness
    
    # Calculating ratios to get right image dimensions
    axial_aspect_ratio = pixel_spacing[1]/pixel_spacing[0]
    sagital_aspect_ratio = pixel_spacing[1]/slices_thickess
    coronal_aspect_ratio = slices_thickess/pixel_spacing[0]
    
    # Creating an empty volume with the correct dimensions
    img_shape = list(slices[0].pixel_array.shape)
    img_shape.append(len(slices))
    volume=np.zeros(img_shape)
    
    # Filling the empty volume with pixel values from each slice
    for i,s in enumerate(slices):
        array2D=s.pixel_array
        volume[:,:,i]= array2D
    
    # Displaying axial view
    axial=plt.subplot(1,3,1)
    plt.title("Axial")
    plt.imshow(volume[:,:,img_shape[2]//2])
    plt.axis("off")
    axial.set_aspect(axial_aspect_ratio)
        
    # Displaying coronal view
    coronal = plt.subplot(1,3,2)
    plt.title("Coronal")
    plt.imshow(volume[img_shape[0]//2,:,:].T)
    plt.axis("off")
    coronal.set_aspect(coronal_aspect_ratio)
    
    # Displaying sagital view
    sagital=plt.subplot(1,3,3)
    plt.title("Sagital")
    plt.imshow(volume[:,img_shape[1]//2,:])
    plt.axis("off")
    sagital.set_aspect(sagital_aspect_ratio)
    
    plt.show()
    