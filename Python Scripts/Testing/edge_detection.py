import cv2
import matplotlib.pyplot as plt
import pydicom as dicom
import numpy as np

# Choose an image to read
img = cv2.imread("./Sample Images/img2.jpg", cv2.IMREAD_GRAYSCALE) # Reading as a grayscale
#img = dicom.dcmread("./Sample Images/img.dcm").pixel_array

# DICOM is uint16 and cv2.Canny doesn't support that
img = np.uint8(img)

# Showing histogram
plt.hist(img.flatten(),100), plt.show()

# User input for threshold values
thr_L = int(input("Lower threshold value: "))
thr_U = int(input("Upper threshold value: "))

# Finding edges
edges = cv2.Canny(img, thr_L, thr_U)

# Showing final result
plt.figure(2)
plt.subplot(1,2,1)
plt.imshow(img), plt.title("Original"), plt.axis("off")
plt.subplot(1,2,2)
plt.imshow(edges), plt.title("After Edge Detection"), plt.axis("off")
plt.show()
