"""
Written by Erlend L. Gundersen
    erlend.l.gundersen@gmail.com
"""

import numpy as np
import cv2
import os
import skfuzzy as fuzz
import pyvista as pv

import noise_tools
import file_tools

# K-Means Clustering
# input: pixels: array of pixels values (e.g. 2D (X, Y) or 3D (X, Y, Z))
# input: k: amount of clusters
# input: color: RGB or grayscale
def k_means(pixels,
            k = 3,
            attempts = 10,
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
            centers = cv2.KMEANS_RANDOM_CENTERS,
            color = False):
    
    print("\nClustering using K-Means...")
    
    # float32 is required by cv2.kmeans()
    pixels = np.float32(pixels)

    # Reshape depentent on colors or not
    if color:
        pixels_f = pixels.reshape(-1,3)
    else:
        pixels_f = pixels.reshape(-1,1)
    
    #   label       = which cluster each pixel belongs to
    #   center      = k allowed pixel values
    #   pixels_f    = flattened pixels
    #   k           = number of classes
    #   criteria    = tells the algoritm when to stop
    #   centers     = initial centroids (KMEANS_RANDOM_CENTERS or KMEANS_PP_CENTERS)
    
    _, label, center = cv2.kmeans(pixels_f, k, None, criteria, attempts, centers)
    
    # Converting back to uint16 (JPEG is uint8, DICOM is uint16)
    center = np.uint16(center) # Array of the k allowed shades of gray
    
    # Creating a flattened pixel array containing the k allowed shades of gray
    pixels_segmented_f = center[label.flatten()]
    
    # Reshaping flattened pixel array to the dimensions of the original image
    return pixels_segmented_f.reshape((pixels.shape)), center


# Fuzzy Clustering
# input: pixels: array of pixels values (e.g. 2D (X, Y) or 3D (X, Y, Z))
# input: k: amount of clusters
# input: color: RGB or grayscale
def FCM(pixels, k = 3, m = 2, error = 0.005, maxiter = 100, color = False):
    
    print("\nClustering using FCM...")
    
    # Converting to float32
    pixels = np.float32(pixels)

    # Reshape depentent on colors or not
    if color:
        pixels_f = pixels.reshape(-1,3)
    else:
        pixels_f = pixels.reshape(-1,1)
    
    # Transposing to fit fuzz.clusters.cmeans()
    pixels_f = pixels_f.T
    
    #   cntr    = each center along each feature provided for every cluster
    #   u       = final fuzzy k-partitioned matrix
    #   k       = number of clusters
    #   m       = fuzziness degree
    #   error   = stop when reaching this error accuracy
    #   maxiter = maximum number of iterations before stopping

    cntr, u, _, _, _, _, _ = fuzz.cluster.cmeans(pixels_f, k, m, error, maxiter, init=None)
    
    # Converting back to uint16 (JPEG is uint8, DICOM is uint16)
    cntr = np.uint16(cntr) # Array of the k allowed shades of gray

    # Selecting the ones at the maximas
    pixels_clustered = np.uint16(np.argmax(u,axis=0)) # argmin to invert

    # Creating flattened array
    pixels_segmented_f = cntr[pixels_clustered]

    # Reshaping flattened pixel array to the dimensions of the original image
    return pixels_segmented_f.reshape((pixels.shape)), cntr


# Creating a 4D array of all the clusters
#  input: labels from clustering (which center each pixel belongs to)
#  input: centers from clustering (k pixel values)
# output: 4D array of the pixels from each individual cluster (cluster, X, Y, Z)
def get_clusters(labels, centers):
    return np.array([np.where(labels != clstr,0,labels) for clstr in centers])


# Save one volume as a 3D file
def save_3d(volume, file_name="3d_object",file_type=".stl",
            denoise=True, largest=False):
    # Denoising
    if denoise:
        volume = noise_tools.denoise_gaussian(volume, 0.5)
    
    # Converting array to mesh
    mesh = pv.wrap(volume)
    
    # Extracting contours
    contours = mesh.contour()
    
    # Extracting the largest connected part
    if largest:
        contours = contours.extract_largest()
    
    # Saving as a file
    contours.save(file_name+file_type)
    

# Save all volumes (e.g. clusters) as 3D files
def save_all_3d(volumes, series_number, folder_name="3D Objects", file_type=".stl",
                denoise=True, largest=False):
    print("Saving files to the folder '"+folder_name+"' as type '"+file_type+"'")
    print("\tDenoise: "+str(denoise))
    print("\tLargest: "+str(largest)+"\n")
    
    
    folder_path = "./"+folder_name
    file_tools.create_folder(folder_path)
    
    for i, volume in enumerate(volumes):
        name = "s"+str(series_number)+"c"+str(i+1)
        print("\t"+name)
        save_3d(volume, file_name=os.path.join(folder_path, name),
                file_type=file_type, denoise=denoise, largest=largest)
        
    print("\tDone.")
    
    
# Function for user input of which cluster(s) to keep
def get_keep():
    # Selecting which clusters to keep
    keep = set()
    N_show = int(input("\tAmount of clusters to show: "))
    while len(keep) < N_show:
        if len(keep) == 0:
            keep.add(int(input("\t\tSelect a cluster: ")))
        else:
            keep.add(int(input("\t\tSelect another cluster: ")))
    print(" ")
    
    return keep
    

# Displaying all clusters from a 4D array of pixels (cluster, X, Y, Z)
def show_all_clusters(clusters, mode="isosurface", opacity=0.25, denoise=True, largest=False):
    print("\nShowing all clusters...")
    print("\tMode:    "+mode)
    print("\tOpacity: "+str(opacity))
    print("\tDenoise: "+str(denoise))
    print("\tLargest: "+str(largest))
    
    # Color options
    cmap = np.array(["cool", "autumn", "winter", "copper", "PiYG", "viridis", "Purples", "Blues", "Greens", "Reds", "Oranges"])
    
    modes = ['isosurface', 'volume']
    if mode not in modes:
        raise ValueError("Invalid mode. Expected one of: %s" % modes)
        
    # Adding labels to the axes
    labels = dict(xlabel='X', ylabel='Y', zlabel='Z')

    # Defining the plot space based on amount of clusters
    shape = str(int(np.ceil(len(clusters)/2)))+"/"+str(int(np.ceil(len(clusters)/2)))
    
    p = pv.Plotter(shape=shape)
    # Denoising
    if denoise:
        clusters = noise_tools.denoise_gaussian(clusters, 0.5)

    for i in range(len(clusters)):
        p.subplot(i)
        p.add_text("Opacity: "+str(opacity)+", Denoise: "+str(denoise)+", Largest: "+str(largest)+"\nMode: "+mode+"\nCluster: "+str(i+1), font_size=14)
        mesh = pv.wrap(clusters[i])
        
        if mode == "isosurface":
            contours = mesh.contour()
            
            # Extract largest
            if largest:
                contours = contours.extract_largest()
                
            p.add_mesh(contours, opacity=opacity, cmap = cmap[i], show_scalar_bar=False)
            
        elif mode == "volume":
            p.add_volume(mesh, opacity=opacity, cmap = cmap[i])
            
        p.show_grid(**labels)
        p.add_axes(**labels)
        p.view_yx()
    
    p.show()
    
    
# Displaying selected cluster(s) from a 4D array of pixels (cluster, X, Y, Z)
def show_individual_clusters(clusters, mode="isosurface", opacity=0.25, denoise=True, largest=True):
    print("\nShowing individual clusters...")
    print("\tMode:    "+mode)
    print("\tOpacity: "+str(opacity))
    print("\tDenoise: "+str(denoise))
    print("\tLargest: "+str(largest))
          
    # Color options
    cmap = np.array(["cool", "autumn", "winter", "copper", "PiYG", "viridis", "Purples", "Blues", "Greens", "Reds", "Oranges"])
    
    modes = ['isosurface', 'volume']
    if mode not in modes:
        raise ValueError("Invalid mode. Expected one of: %s" % modes)
        
    
    # Adding labels to the axes
    labels = dict(xlabel='X', ylabel='Y', zlabel='Z')
          
    # Selecting which clusters to keep by user input
    keep = get_keep()

    # Denoising
    if denoise:
        clusters = noise_tools.denoise_gaussian(clusters, 0.5)

    p = pv.Plotter()
    p.add_text("Opacity: "+str(opacity)+", Denoise: "+str(denoise)+", Largest: "+str(largest)+"\nMode: "+mode+"\nCluster(s): "+str(keep), font_size=14)

    for i in keep:
        mesh = pv.wrap(clusters[i-1])
            
        if mode == "isosurface":
            contours = mesh.contour()
        
            # Extract largest
            if largest:
                contours = contours.extract_largest()
                
            p.add_mesh(contours, opacity=opacity, cmap = cmap[i], show_scalar_bar=False)
            
        elif mode == "volume":
            p.add_volume(mesh, opacity=opacity, cmap = cmap[i])
            
        p.show_grid(**labels)
        p.add_axes(**labels)
        p.view_yx()
        
    p.show()
            
       
# Thresholding and displaying a 3D array (X, Y, Z) of pixel values
def threshold_sliders(volume, opacity=None, denoise=False, largest=True):
    print("\nStarting thresholding tool with sliders...")
    print("\tOpacity: "+str(opacity))
    print("\tDenoise: "+str(denoise))
    print("\tLargest: "+str(largest))
    
    # Initializing threshold limits
    global thr_L
    global thr_U
    thr_L = np.min(volume)
    thr_U = np.max(volume)
    
    # Denoising
    if denoise:
        volume = noise_tools.denoise_gaussian(volume, 0.5)

    # Initializing plot window
    p = pv.Plotter()
    p.add_text("Opacity: "+str(opacity)+", Denoise: "+str(denoise)+", Largest: "+str(largest)+"\nMode: thresholding", font_size=14)

    # Create mesh
    mesh = pv.wrap(volume)

    # Isosurface
    contours = mesh.contour()
    
    # Extract largest
    if largest:
        contours = contours.extract_largest()

    # Add structure to plot
    p.add_mesh(contours, opacity=opacity, name="123", show_scalar_bar=False)
    # (When assigning a new mesh with the same name (123), it will overwrite the
    #  previous one. This is done in the create_thr_L/U_mesh functions!)

    # Adding grid and labels
    labels = dict(xlabel='X', ylabel='Y', zlabel='Z')
    p.show_grid(**labels)
    p.add_axes(**labels)
    p.view_yx()

    # Function that is executed every time the lower limit slider is used
    def create_thr_L_mesh(value):
        global thr_L # lower limit
        thr_L = value
    
        # Thresholding
        thr = mesh.threshold([thr_L, thr_U])
    
        # Isosurface
        contours = thr.contour()
    
        # Extract largest
        if largest:
            contours = contours.extract_largest()
    
        p.add_mesh(contours, opacity=opacity, name="123", show_scalar_bar=False)
        return

    # Function that is executed every time the upper limit slider is used
    def create_thr_U_mesh(value):
        global thr_U # upper limit
        thr_U = value
    
        # Thresholding
        thr = mesh.threshold([thr_L, thr_U])
    
        # Isosurface
        contours = thr.contour()
        
        # Extract largest
        if largest:
            contours = contours.extract_largest()
    
        # Add structure to plot
        p.add_mesh(contours, opacity=opacity, name="123", show_scalar_bar=False)
        return

    # Adding widgets to the plotter
    p.add_slider_widget(create_thr_L_mesh,
                        rng = [np.min(volume), np.max(volume)],
                        title = 'Lower Threshold Limit',
                        value = np.min(volume),
                        pointa = (.75, .775), pointb = (.975, .775))

    p.add_slider_widget(create_thr_U_mesh,
                        rng = [np.min(volume), np.max(volume)],
                        value = np.max(volume),
                        title = 'Upper Threshold Limit',
                        pointa = (.75, .925), pointb = (.975, .925))

    p.show()