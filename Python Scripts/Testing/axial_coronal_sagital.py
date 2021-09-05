import matplotlib.pyplot as plt
import pydicom as dicom
import numpy as np
import os

# Selecting folder and storing filenames as a list of strings
path = "./Sample Images/Sample Series/"
file_names=os.listdir(path)

# Importing each DICOM file as a slice
slices = [dicom.dcmread(os.path.join(path,file_name)) for file_name in file_names]

# Sorting the slices
slices = sorted(slices,key=lambda x:x.ImagePositionPatient[2])

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
volume3d=np.zeros(img_shape)

# Filling the empty volume with pixel values from each slice
for i,s in enumerate(slices):
    array2D=s.pixel_array
    volume3d[:,:,i]= array2D
    
#%% Plotting

# Displaying Axial
axial=plt.subplot(1,3,1)
plt.title("Axial")
plt.imshow(volume3d[:,:,img_shape[2]//2]), plt.axis("off")
axial.set_aspect(axial_aspect_ratio)

# Displaying Coronal
coronal = plt.subplot(1,3,2)
plt.title("Coronal")
plt.imshow(volume3d[img_shape[0]//2,:,:].T), plt.axis("off")
coronal.set_aspect(coronal_aspect_ratio)

# Displaying Sagital
sagital=plt.subplot(1,3,3)
plt.title("Sagital")
plt.imshow(volume3d[:,img_shape[1]//2,:]), plt.axis("off")
sagital.set_aspect(sagital_aspect_ratio)

plt.show()

print("Array2D.shape:\t",array2D.shape)
print("volume3d.shape:\t",volume3d.shape) 