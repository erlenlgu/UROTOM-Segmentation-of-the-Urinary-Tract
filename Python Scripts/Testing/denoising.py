# Multichannel may have to be changed for grayscale or DICOM

import matplotlib.pyplot as plt
import numpy as np
import pydicom as dicom

# Choose an image to process
#img = plt.imread('./Sample Images/Lena_noisy.png')
img = plt.imread('./Sample Images/img2.jpg')
#img = dicom.dcmread('./Sample Images/img.dcm').pixel_array

# Converting to grayscale
from skimage import color
img = color.rgb2gray(img)

# Converting to float
from skimage import img_as_float
img = img_as_float(img)

plt.imshow(img), plt.title("Original")
plt.axis("off"), plt.show()

#%% Denoising and plotting

# Gaussian Smoothing (blurry...)
from scipy import ndimage as nd
gaussianImg = nd.gaussian_filter(img, sigma = 3)
plt.imshow(gaussianImg), plt.title("Gaussian smoothing")
plt.axis("off"), plt.show()

# Bilateral (SLOW!!! DON'T USE UT)
from skimage.restoration import denoise_bilateral
bilateralImg = denoise_bilateral(img, sigma_spatial = 10, multichannel = False)
plt.imshow(bilateralImg), plt.title("Bilateral")
plt.axis("off"), plt.show()

# TV
from skimage.restoration import denoise_tv_chambolle
TVImg = denoise_tv_chambolle(img, weight = 0.3, multichannel = False)
plt.imshow(TVImg), plt.title("Denoise TV")
plt.axis("off"), plt.show()

# Wavelet
from skimage.restoration import denoise_wavelet
waveletImg = denoise_wavelet(img, multichannel = True, method= "BayesShrink", mode = "soft", rescale_sigma = False)
plt.imshow(waveletImg), plt.title("Wavelet")
plt.axis("off"), plt.show()

# Anisotropic Diffusion
from medpy.filter.smoothing import anisotropic_diffusion
anisotropicDiffusionImg = anisotropic_diffusion(img, niter = 50, kappa = 50, gamma = 0.2, option = 2)
plt.imshow(anisotropicDiffusionImg), plt.title("Anisotropic Diffusion")
plt.axis("off"), plt.show()

# NL means
from skimage.restoration import denoise_nl_means
from skimage.restoration import estimate_sigma
sigma_est = np.mean(estimate_sigma(img, multichannel=False))
NlMeansImg = denoise_nl_means(img, h = 1.15 * sigma_est, fast_mode = True, patch_size = 9, patch_distance = 5, multichannel = False)
plt.imshow(NlMeansImg), plt.title("NL Means")
plt.axis("off"), plt.show()

# BM3D (seems very good!)
import bm3d
bm3dImg = bm3d.bm3d(img, sigma_psd = 0.2, stage_arg = bm3d.BM3DStages.ALL_STAGES)
plt.imshow(bm3dImg), plt.title("BM3D")
plt.axis("off"), plt.show()

#%% One figure with subplots of all

plt.figure(99)
plt.subplot(2,4,1)
plt.imshow(img), plt.title("Original"), plt.axis("off")
plt.subplot(2,4,2)
plt.imshow(gaussianImg), plt.title("Gaussian smoothing"), plt.axis("off")
plt.subplot(2,4,3)
plt.imshow(bilateralImg), plt.title("Bilateral"), plt.axis("off")
plt.subplot(2,4,4)
plt.imshow(TVImg), plt.title("Denoise TV"), plt.axis("off")
plt.subplot(2,4,5)
plt.imshow(waveletImg), plt.title("Wavelet"), plt.axis("off")
plt.subplot(2,4,6)
plt.imshow(anisotropicDiffusionImg), plt.title("Anisotropic Diffusion"), plt.axis("off")
plt.subplot(2,4,7)
plt.imshow(NlMeansImg), plt.title("NL Means"), plt.axis("off")
plt.subplot(2,4,8)
plt.imshow(bm3dImg), plt.title("BM3D"), plt.axis("off")
plt.show()
