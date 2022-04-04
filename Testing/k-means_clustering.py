import numpy as np
import cv2
import matplotlib.pyplot as plt
import pydicom as dicom

cmap = "gray"

# Reading images
img_jpg = cv2.imread("./Sample Images/img2.jpg", cv2.IMREAD_GRAYSCALE) # Reading as a grayscale
img_dcm = dicom.dcmread("./Sample Images/img.dcm").pixel_array

#%% Defining the K-Means Clustering
def k_means(img,
            k = 3,
            attempts = 10,
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
            centers = cv2.KMEANS_RANDOM_CENTERS,
            color = False):
    
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
    return img_segmented_f.reshape((img.shape))

#%% K-Means Clustering for the JPEG image
k = 3
attempts = 10
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
centers = cv2.KMEANS_PP_CENTERS # or cv.KMEANS_RANDOM_CENTERS

img_jpg_segmented = k_means(img_jpg, k, attempts, criteria, color=False)

# Plotting
plt.figure(1)
plt.subplot(1,2,1), plt.imshow(img_jpg, cmap), plt.axis("off"), plt.title("Original")
plt.subplot(1,2,2), plt.imshow(img_jpg_segmented, cmap), plt.axis("off"), plt.title("k="+str(k))
plt.show()

#%% K-Means Clustering for the DICOM image
k = 3
attempts = 10
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
centers = cv2.KMEANS_PP_CENTERS # or cv.KMEANS_RANDOM_CENTERS

img_dcm_segmented = k_means(img_dcm, k, attempts, criteria, color=False)

# Plotting
plt.figure(1)
plt.subplot(1,2,1), plt.imshow(img_dcm, cmap), plt.axis("off"), plt.title("Original")
plt.subplot(1,2,2), plt.imshow(img_dcm_segmented, cmap), plt.axis("off"), plt.title("k="+str(k))
plt.show()

