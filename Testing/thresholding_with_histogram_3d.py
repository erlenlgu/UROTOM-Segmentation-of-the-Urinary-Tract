import numpy as np
import matplotlib.pyplot as plt
import pydicom as dicom
import os
import pyvista as pv
import sys

# Giving access to the Tools folder
sys.path.insert(0, '../Tools')

import dcm_tools
import noise_tools

# Array of color options
cmap = np.array(["cool", "autumn", "winter", "copper", "PiYG", "viridis", "Purples", "Blues", "Greens", "Reds", "Oranges"])

# Selecting folder and storing filenames as a list of strings
path = "./Sample Images/Sample Series/"
#path = "./Sample Images/CT/"
file_names=os.listdir(path)

# Importing dicoms from each filepath in path
print("Loading files...")
dicoms = np.array([dicom.dcmread(os.path.join(path,file_name)) for file_name in file_names])

# Convert list of dicoms to 3D volume (with interpolation, etc.)
volume = dcm_tools.get_volume(dicoms)

volume = np.flip(volume,0) # Fix x direction
    
# Denoising (better after thresholding?)
#print("Denoising...")
#volume = noise_tools.denoise_gaussian(volume, 0.5)
#volume = noise_tools.denoise_bm3d(volume)

#%% Histogram
plt.figure(1)
plt.rcParams.update({'font.size': 22}) # Increase font size
plt.hist(volume.flatten(), bins=100), plt.title("Histogram of original")
plt.yscale("log")
plt.xlabel("Pixel Value"), plt.ylabel("Frequency [log]")
plt.show()

#%% Plotting
print("\nPlotting...")

labels = dict(zlabel='Z [mm]', xlabel='X [mm]', ylabel='Y [mm]')

# Initializing threshold limits
thr_L = np.min(volume)
thr_U = np.max(volume)

# Initializing plot window
p = pv.Plotter()
p.add_text("Thresholding...", font_size=14)

# Create mesh
mesh = pv.wrap(volume)

# Isosurface
contours = mesh.contour()

# Add structure to plot
p.add_mesh(contours, name="123")#opacity="linear")

# Adding grid and labels
p.show_grid(**labels)
p.add_axes(**labels)
p.view_yx()

def create_thr_L_mesh(value):
    global thr_L
    thr_L = value
    
    # Thresholding
    thr = mesh.threshold([thr_L, thr_U])
    
    # Isosurface
    contours = thr.contour()
    
    #largest = contours.connectivity(largest=True)
    
    p.add_mesh(contours, name="123")#, opacity="linear")
    return

def create_thr_U_mesh(value):
    global thr_U
    thr_U = value
    
    # Thresholding
    thr = mesh.threshold([thr_L, thr_U])
    
    # Isosurface
    contours = thr.contour()
    
    # Add structure to plot
    p.add_mesh(contours, name="123")#, opacity="linear")
    return

p.add_slider_widget(create_thr_L_mesh,
                    rng = [np.min(volume), np.max(volume)],
                    title = 'Lower Threshold Limit',
                    value = np.min(volume),
                    pointa = (.15, .9), pointb = (.35, .9))

p.add_slider_widget(create_thr_U_mesh,
                    rng = [np.min(volume), np.max(volume)],
                    value = np.max(volume),
                    title = 'Upper Threshold Limit',
                    pointa = (.65, .9), pointb = (.85, .9))

p.show()


#%% Only show the largest connecting part
print("\nLargest connecting part only...")

# Initializing threshold limits
thr_L = np.min(volume)
thr_U = np.max(volume)

# Initializing plot window
p = pv.Plotter()
p.add_text("Largest connecting part after thresholding...", font_size=14)

# Create mesh
mesh = pv.wrap(volume)

# Isosurface
contours = mesh.contour()

largest = contours.connectivity(largest=True)

# Add structure to plot
p.add_mesh(largest, name="123")#opacity="linear")

# Adding grid and labels
p.show_grid(**labels)
p.add_axes(**labels)
p.view_yx()

def create_thr_L_mesh(value):
    global thr_L
    thr_L = value
    
    # Thresholding
    thr = mesh.threshold([thr_L, thr_U])
    
    # Isosurface
    contours = thr.contour()
    
    largest = contours.connectivity(largest=True)
    
    p.add_mesh(largest, name="123")#, opacity="linear")
    return

def create_thr_U_mesh(value):
    global thr_U
    thr_U = value
    
    # Thresholding
    thr = mesh.threshold([thr_L, thr_U])
    
    # Isosurface
    contours = thr.contour()
    
    largest = contours.connectivity(largest=True)
    
    # Add structure to plot
    p.add_mesh(largest, name="123")#, opacity="linear")
    return

p.add_slider_widget(create_thr_L_mesh,
                    rng = [np.min(volume), np.max(volume)],
                    title = 'Lower Threshold Limit',
                    value = np.min(volume),
                    pointa = (.15, .9), pointb = (.35, .9))

p.add_slider_widget(create_thr_U_mesh,
                    rng = [np.min(volume), np.max(volume)],
                    value = np.max(volume),
                    title = 'Upper Threshold Limit',
                    pointa = (.65, .9), pointb = (.85, .9))

p.show()


