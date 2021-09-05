import numpy as np
import cv2
import matplotlib.pyplot as plt
import pydicom as dicom
import skfuzzy as fuzz

cmap = "gray"

# Reading images
img_jpg = cv2.imread("./Sample Images/img2.jpg", cv2.IMREAD_GRAYSCALE) # Reading as a grayscale
img_dcm = dicom.dcmread("./Sample Images/img.dcm").pixel_array

#%% Defining the Fuzzy Clustering
def FCM(img, k = 3, m = 2, error = 0.005, maxiter = 100, color = False):
    
    # Converting to float32 (not needed...)
    img = np.float32(img)

    # Reshape depentent on colors or not
    if color:
        img_f = img.reshape(-1,3)
    else:
        img_f = img.reshape(-1,1)
    
    # Transposing to fit fuzz.clusters.cmeans()
    img_f = img_f.T
    
    #   cntr    = each center along each feature provided for every cluster
    #   u       = final fuzzy k-partitioned matrix
    #   k       = number of clusters
    #   m       = fuzziness degree
    #   error   = stop when reaching this error accuracy
    #   maxiter = maximum number of iterations before stopping

    cntr, u, _, _, _, _, _ = fuzz.cluster.cmeans(img_f, k, m, error, maxiter, init=None)
    
    # Converting back to uint16 (JPEG is uint8, DICOM is uint16)
    cntr = np.uint16(cntr) # Array of the k allowed shades of gray

    # Using membership function to classify
    img_clustered = np.uint16(np.argmax(u,axis=0)) # argmin to invert

    # Getting 
    img_segmented_f = cntr[img_clustered]

    # Reshaping flattened pixel array to the dimensions of the original image
    return img_segmented_f.reshape((img.shape))

#%% Fuzzy Clustering for the JPEG image
k = 3 # clusters
m = 2 # fuzziness degree (2)
error = 0.005
maxiter = 100

img_jpg_segmented = FCM(img_jpg, k, m, error, maxiter, color=False)

# Plotting
plt.subplot(1,2,1), plt.imshow(img_jpg, cmap), plt.axis("off"), plt.title("Original")
plt.subplot(1,2,2), plt.imshow(img_jpg_segmented, cmap), plt.axis("off")
plt.title("k="+str(k)+", Fuzziness Degree: "+str(m))
plt.show()

#%% Fuzzy Clustering  for the DICOM image
k = 3 # clusters
m = 2 # fuzziness degree (2)
error = 0.005
maxiter = 100

img_dcm_segmented = FCM(img_dcm, k, m, error, maxiter, color=False)

# Plotting
plt.subplot(1,2,1), plt.imshow(img_dcm, cmap)
plt.title("Original"), plt.axis("off")
plt.subplot(1,2,2), plt.imshow(img_dcm_segmented, cmap)
plt.title("k="+str(k)+", Fuzziness Degree: "+str(m)), plt.axis("off")
plt.show()
