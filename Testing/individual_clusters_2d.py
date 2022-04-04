import numpy as np
import cv2
import matplotlib.pyplot as plt
import pydicom as dicom
import sys

# Giving access to the Tools folder
sys.path.insert(0, '../Tools')

import dcm_tools

cmap = "gray"

# Reading image
dcm = dicom.dcmread("./Sample Images/img.dcm")

# Sample image from the internet (CT)
#dcm = dicom.dcmread("./Sample Images/CT/image-000001.dcm")

img = dcm_tools.get_pixels_reshaped(dcm)

# Settings
k = 5
attempts = 10
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
centers = cv2.KMEANS_RANDOM_CENTERS
color = False
    
# float32 is required by cv2.kmeans()
img = np.float32(img)

# Reshape depentent on colors or not
if color:
    img_f = img.reshape(-1,3)
else:
    img_f = img.reshape(-1,1)

#   label       = which cluster each pixel belongs to
#   center      = k allowed pixel values
#   img_f       = flattened image
#   k           = number of classes
#   criteria    = tells the algoritm when to stop
#   centers     = initial centroids (KMEANS_RANDOM_CENTERS or KMEANS_PP_CENTERS)

_, label, center = cv2.kmeans(img_f, k, None, criteria, attempts, centers)

# Converting back to uint16 (JPEG is uint8, DICOM is uint16)
center = np.uint16(center) # Array of the k allowed shades of gray
    
# Creating a flattened pixel array containing the k allowed shades of gray
img_segmented_f = center[label.flatten()]
    
# Reshaping flattened pixel array to the dimensions of the original image
image_segmented = img_segmented_f.reshape((img.shape))

# Showing the original and the segmented one
plt.subplot(1,2,1), plt.imshow(img, cmap), plt.title("Original")
plt.subplot(1,2,2), plt.imshow(image_segmented, cmap), plt.title("k="+str(k))

# Showing only one cluster at once
for i in range(len(center)):
    image_seg_one = np.where(image_segmented != center[i],0,image_segmented)

    # Plotting
    plt.subplot(1,2,1), plt.imshow(image_segmented, cmap), plt.title("k="+str(k))
    plt.subplot(1,2,2), plt.imshow(image_seg_one, cmap), plt.title("Cluster:"+str(i+1))
    plt.show()