"""
Written by Erlend L. Gundersen
    erlend.l.gundersen@gmail.com
"""

from scipy import ndimage as nd
import bm3d


# Gaussian smoothing of a noisy input (e.g. an image or a 3D array)
def denoise_gaussian(noisy_input, sigma = 1):
    return nd.gaussian_filter(noisy_input, sigma)


# BM3D denoising of a noisy input (e.g. an image or a 3D array)
def denoise_bm3d(noisy_input, sigma_psd = 0.02):#, stage_arg = bm3d.BM3DStages.ALL_STAGES):
    return bm3d.bm3d(noisy_input, sigma_psd)#, stage_arg)


"""
# SOME OTHER METHODS:
    
# Bilateral (SLOW!!!)
from skimage.restoration import denoise_bilateral
bilateralImg = denoise_bilateral(img, sigma_spatial = 10, multichannel = False)

# TV
from skimage.restoration import denoise_tv_chambolle
TVImg = denoise_tv_chambolle(img, weight = 0.3, multichannel = False)

# Wavelet
from skimage.restoration import denoise_wavelet
waveletImg = denoise_wavelet(img, multichannel = True, method= "BayesShrink", mode = "soft", rescale_sigma = False)

# Anisotropic Diffusion
from medpy.filter.smoothing import anisotropic_diffusion
anisotropicDiffusionImg = anisotropic_diffusion(img, niter = 50, kappa = 50, gamma = 0.2, option = 2)

# NL means
from skimage.restoration import denoise_nl_means
from skimage.restoration import estimate_sigma
sigma_est = np.mean(estimate_sigma(img, multichannel=False))
NlMeansImg = denoise_nl_means(img, h = 1.15 * sigma_est, fast_mode = True, patch_size = 9, patch_distance = 5, multichannel = False)
"""