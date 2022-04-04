Written by Erlend Løland Gundersen  
    erlend.l.gundersen@gmail.com

# UROTOM-Segmentation-of-the-Urinary-Tract

The code was written during my internship about Image Processing and Analysis  
at Lodz University of Technology, Institute of Applied Computer Science.

Medical Imaging Project: UROTOM  
• System of Noninvasive Monitoring and Diagnosis of the Lower Urinary Tract  
• Segmentation, Noise Reduction, and Three-Dimensional Visualization of DICOMs using Python and ML

# INITIAL NOTES:

    1. main.py demonstrates the most important functions
    2. The "Tools" folder contains modules used in both main.py and "Testing"
    3. main.py runs without scipts from "Testing"
    4. Follow instructions in the command window
    5. Rotating series such as series 1104 in folder J_A are not supported yet
    6. Fuzzy clustering is really slow, and k-means gave very similar results
         
        
# INSTRUCTIONS:

    0. Install necessary Python libraries (list at the bottom)
    1. Enter path to the folder of zip files (e.g. !!DICOM) in main.py
    2. Run the SETUP AND IMPORT section
    3. Run the LOADING section and select a folder and a series of dicoms
    4. Change the parameters (mode, opacity, denoise and largest) in the script


# IMPORTANT VARIABLES:

             dicoms     list of objects (pydicom.dataset modules)
             volume     3D array of pixel values (X, Y, Z)
              
                  k     amount of clusters
            centers     centers in the clustering (k grayscale values)
             labels     3D array of which center each pixel value belongs to
           clusters     4D array of individual clusters (cluster, X, Y, Z)
           

# TOOLS (modules):
 
                   dcm_tools     dicom related helper functions
               display_tools     displaying collages, slideshows, histograms, etc.
                 noise_tools     denoising functions like Gaussian smoothing, BM3D, etc.
                  file_tools     unzipping, create folder, directory paths dictionary...
          segmentation_tools     clustering and thresholding  
          
 # IMPORTANT PARAMETERS:

 **These are used in show_all_clusters(), show_individual_clusters(),
   save_all_3d() and threshold_sliders(). (see more info below.)**

                        mode     type of rendering ("isosurface" or "volume")
                     opacity     degree of transparency (e.g. "linear, 0.25, None...")
                     denoise     denoise or not with Gaussian smoothing (True/False)
                     largest     only display the largest connected body (True/False)
                                 - largest is not supported when mode = "volume"

                                       
# IMPORTANT FUNCTIONS:

  **From dcm_tools:**
 
  dicoms_from_path_of_zips()     select and load dicom series from folder of zips                                                
                get_volume()     interpolated volume from list of dicom objects
                get_pixels()     array of pixel values from list of dicom objects

  **From segmentation_tools:**
                   
                   k_means()     clustering pixels array and returns labels and centers
                       FCM()     clustering pixels array and returns labels and centers
              get_clusters()     get 4D clusters array from labels and centers
         show_all_clusters()     display all clusters in a 4D clusters array
  show_individual_clusters()     display selected clusters in a 4D clusters array
               save_all_3d()     save all clusters in 4D clusters array as 3D models
         threshold_sliders()     display a thresholded version of a volume (with sliders)
         
   **From display_tools:**
                      
   show_axial_coronal_sagital()     display the dicom series from three angles   
               show_histogram()     display histogram of a volume with pixel values  
                     show_all()     display all images in an array of images one by one   
                     
# TESTING: 

    # The "Testing" folder contains scripts used while making functions in "Tools"
    # File type conversion (e.g. to jpeg), edge detection, header manipulation...


# VERSIONS:
                             
             Python     3.8.8
      Anaconda Nav.	    2.0.3
             Spyder     4.2.5

 # Libraries required for main.py and "Tools" modules:
 
              numpy     1.20.2	   fast handling of arrays
         matplotlib  	3.3.4	   simple plotting
             pillow     8.2.0      image handler
           openjpeg     2.3.0      decompress dicom files
            pydicom     2.1.2	   handling dicom files	
            pyvista     0.31.3     3D visualization
              scipy	    1.6.2	   denoising	
       scikit-fuzzy 	0.4.2	   fuzzy clustering	
      opencv-python  	4.5.2.54   k-Means clustering
      
      # NOTE: openjpeg and pillow have to be installed in the right order

 # Libraries only used in scripts from the "Testing" folder:
 
        scikit-image    0.18.1  denoising
                bm3d    3.0.9   denoising
               medpy    0.4.0   denoising
              plotly    5.1.0   fast plotting
                                  
