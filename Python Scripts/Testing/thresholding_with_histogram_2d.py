import pydicom as dicom
import matplotlib.pyplot as plt
import cv2
import sys

# Giving access to the Tools folder
sys.path.insert(0, '../Tools')

import dcm_tools

# Reading DICOM file
dcm = dicom.dcmread('./Sample Images/img.dcm')

img = dcm_tools.get_pixels_reshaped(dcm)

# Histogram and plotting
plt.figure(1)

plt.hist(img.flatten(), bins=100), plt.title("Histogram of original")
plt.xlabel("Pixel Value"), plt.ylabel("Frequency")
plt.show()

plt.figure(2)

plt.subplot(1,3,1), plt.xlabel("[mm]"), plt.ylabel("[mm]") 
plt.imshow(img), plt.title("Original")

_, img_thr = cv2.threshold(img,890,970,cv2.THRESH_BINARY)
plt.subplot(1,3,2), plt.xlabel("[mm]"), plt.ylabel("[mm]")
plt.imshow(img_thr), plt.title("Threshold: 890-970")

_, img_thr_2 = cv2.threshold(img,1050,1085,cv2.THRESH_BINARY)
plt.subplot(1,3,3), plt.xlabel("[mm]"), plt.ylabel("[mm]")
plt.imshow(img_thr_2), plt.title("Threshold: 1050-1085")

plt.show()