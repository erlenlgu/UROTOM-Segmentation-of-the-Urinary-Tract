import numpy as np
import cv2
import os
import sys
import pydicom as dicom
import pyvista as pv

# Giving access to the Tools folder
sys.path.insert(0, '../Tools')

import dcm_tools
import segmentation_tools
import noise_tools
import display_tools


# Settings for clustering
k = 6
#k = int(input("Select amount of clusters: "))

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
    
# Fix x direction
volume = np.flip(volume, 0)
    
# Denoising (better after clustering?)
#print("Denoising...")
#volume = noise_tools.denoise_gaussian(volume, 0.5)
#volume = noise_tools.denoise_bm3d(volume)
    
# Clustering the 3D array
pixels, centers = segmentation_tools.k_means(volume, k)
#pixels, centers = segmentation_tools.FCM(volume, k)

# 4D Array of all the clusters
clusters = np.array([np.where(pixels != clstr,0,pixels) for clstr in centers])
print("\tDone.")

# Adding labels to the axes
labels = dict(zlabel='Z [mm]', xlabel='X [mm]', ylabel='Y [mm]')

# Defining the plot space based on amount of clusters
shape = str(int(np.ceil(k/2)))+"/"+str(int(np.ceil(k/2)))

#%% ISOSURFACES
print("\nSTARTING ISOSURFACES...")

p = pv.Plotter(shape=shape)
for i in range(k):
    p.subplot(i)
    p.add_text("Cluster: "+str(i+1), font_size=14)
    mesh = pv.wrap(clusters[i])
    contours = mesh.contour()
    p.add_mesh(contours, cmap = cmap[i])#, opacity="linear") #opacity = 0.25
    p.show_grid(**labels)
    p.add_axes(**labels)
    p.view_yx()
    
p.show()

#%% Show clusters as isosurfaces on top of each other (using pyvista)

# Selecting which clusters to keep
keep = display_tools.get_keep()
    
# Denoising
clusters = noise_tools.denoise_gaussian(clusters, 0.5)

# Adding labels to the axes
labels = dict(zlabel='Z [mm]', xlabel='X [mm]', ylabel='Y [mm]')

p = pv.Plotter()
p.add_text("Clusters: "+str(keep), font_size=14)

for i in keep:
        
    # Convert 3D array to mesh
    mesh = pv.wrap(clusters[i])
        
    # Isosurface
    contours = mesh.contour()

    p.add_mesh(contours, cmap=cmap[i], opacity="linear") #opacity 0.25
    p.show_grid(**labels)
    p.add_axes(**labels)
    p.view_yx()
    #contours.save("isosurface.vtk")

p.show()
        
#%% Show largest part of clusters as isosurfaces on top of each other (using pyvista)

p = pv.Plotter()
p.add_text("Clusters: "+str(keep), font_size=14)

for i in keep:
        
    # Convert 3D array to mesh
    mesh = pv.wrap(clusters[i])
        
    # Isosurface
    contours = mesh.contour()
        
    # Extract largest
    largest = contours.connectivity(largest=True)

    p.add_mesh(largest, cmap=cmap[i])
    p.show_grid(**labels)
    p.add_axes(**labels)
    p.view_yx()
    #contours.save("isosurface.vtk")

p.show()

#%% Show clusters as isosurfaces slide select (using pyvista)
p = pv.Plotter()
p.add_text("Clusters select with slider", font_size=14)

mesh = pv.wrap(clusters[0])

contours = mesh.contour()

p.add_mesh(contours, name="123", opacity="linear") #opacity 0.25

p.show_grid(**labels)
p.add_axes(**labels)
p.view_yx()

def create_mesh(value):
    
    mesh = pv.wrap(clusters[int(np.floor(value))])
    contours = mesh.contour()
    
    p.add_mesh(contours, name="123", opacity="linear", cmap="hot")
    return

p.add_slider_widget(create_mesh,
                    rng = [0.9, len(clusters)-0.1],
                    value = 0,
                    title = 'Cluster Select',
                    pointa = (.05, .9), pointb = (.95, .9)
                    )

p.show()

#%% Show clusters as isosurfaces button select (using pyvista)
class SetVisibilityCallback:
    """Helper callback to keep a reference to the actor being modified."""
    def __init__(self, actor):
        self.actor = actor

    def __call__(self, state):
        self.actor.SetVisibility(state)

p = pv.Plotter()
p.add_text("Clusters select with buttons, opacity = linear", font_size=14)

for i in range(len(clusters)):
    
    mesh = pv.wrap(clusters[i])
    contours = mesh.contour()
    
    # INVERT THE BUTTONS PLEASE TO DO!!
    actor = p.add_mesh(contours, opacity="linear")
    
    # Make a separate callback for each widget
    callback = SetVisibilityCallback(actor)
    p.add_checkbox_button_widget(callback, value=True,
                                     position=(10+i*75,670),
                                     size=50,
                                     border_size=1)

    p.show_grid(**labels)
    p.add_axes(**labels)
    p.view_yx()
        

p.show()

#%% VOLUME RENDERING
print("\nSTARTING VOLUME RENDERING...")

#%% Exit or not
def quit_or_not():
    decision = "0"
    while decision != "y" and decision != "n":
        decision = input("Do you want to continue? (y/n): ")
        if decision == "n":
            sys.exit()
            
quit_or_not()
        
#%% Show all clusters volume render (using pyvista)
p = pv.Plotter(shape=shape)
for i in range(k):
    p.subplot(i)
    p.add_text("Clusters: "+str(i+1), font_size=14)
    data = pv.wrap(clusters[i])
    p.add_volume(data, cmap=cmap[i], opacity="linear")
    p.show_grid(**labels)
    p.add_axes(**labels)
    p.view_yx()
    
p.show()

#%% Show clustersvolume render on top of each other (using pyvista)

# Selecting which clusters to keep
keep = display_tools.get_keep()
    
p = pv.Plotter()
for i in keep:
    p.add_text("Clusters: "+str(keep), font_size=14)
    data = pv.wrap(clusters[i])
    p.add_volume(data, cmap = cmap[i], opacity="linear")
    p.show_grid(**labels)
    p.add_axes(**labels)
    p.view_yx()

p.show()


#%% Alternatives
print("\nAlternative methods using plotly...")
quit_or_not()

from plotly.offline import plot
import plotly.graph_objects as go

#%% Scatterplot (using plotly)

clstr = int(input("Select a cluster to show: "))

cluster = clusters[clstr]

z, x, y = np.where(cluster==centers[clstr])

fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z,
                                   mode='markers',
                                   marker=dict(
                                       size=1,
                                       opacity=0.6)
                                   )])

plot(fig)

#%% Marching cubes (using plotly)

from plotly.offline import plot
import plotly.graph_objects as go
from skimage import measure
from plotly import figure_factory


def make_mesh(image, step_size=1):

    # Fix orientation
    p = image.transpose(2,1,0)
    
    verts, faces, norm, val = measure.marching_cubes(p, step_size=step_size, allow_degenerate=True) 
    return verts, faces

def plotly_3d(verts, faces):
    x, y, z = zip(*verts) 
    
    print("Drawing...")
    
    # Make the colormap single color since the axes are positional not intensity. 
    colormap=['rgb(236, 236, 212)','rgb(236, 236, 212)']
    
    fig = figure_factory.create_trisurf(x=x,
                            y=y, 
                            z=z, 
                            plot_edges=False,
                            colormap=colormap,
                            simplices=faces,
                            backgroundcolor='rgb(64, 64, 64)',
                            title="Interactive Visualization"
                            )
    plot(fig)


v, f = make_mesh(cluster, 2)
#v, f = make_mesh(volume)
plotly_3d(v, f)
