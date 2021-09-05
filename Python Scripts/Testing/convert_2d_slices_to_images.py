import os
import matplotlib.pyplot as plt
import sys

# Giving access to the Tools folder
sys.path.insert(0, '../Tools')

import file_tools
import dcm_tools

# Enter path of folder with zip files
load_path = "C:/Users/Erlend/Desktop/!!DICOM/"

# Enter path where converted images should be saved
# (A folder will be generated.)
save_path = "C:/Users/Erlend/Desktop/"

print("ENTER PATHS IN SCRIPT BEFORE RUNNING!\n")

# Converting and saving everything in a given folder
def convert_all_in_folder(load_path = ".", save_path = ".", folder_number = 0, file_type='.jpg'):
        
    dic = file_tools.path_dic(load_path)
    for paths in dic["file_paths"][folder_number:folder_number+1]:
        print("Folder: "+dic["folder_names"][folder_number])
    
        # Creating a folder for converted files
        converted_path = os.path.join(save_path,"Converted Images")
        file_tools.create_folder(converted_path)
    
        # Creating a folder for each zip file
        folder_path = os.path.join(converted_path,dic["folder_names"][folder_number])
        file_tools.create_folder(folder_path)
    
        # Loading dicom files from paths and sorting by series
        dicoms = dcm_tools.get_array(paths)
        dicoms_sorted = dcm_tools.series_sort(dicoms)
        
        for SeriesNumber in dicoms_sorted:
            print("\tSeries: "+str(SeriesNumber))
            pixels = dcm_tools.get_pixels(dicoms_sorted[SeriesNumber])
        
            # Creating a folder for each series
            series_path = os.path.join(folder_path,str(SeriesNumber))
            file_tools.create_folder(series_path)
        
            for i in range(len(pixels)):
                plt.imsave(os.path.join(series_path,str(i)+file_type), pixels[i])
         
         
# Converting and saving everything in all folders
def convert_all(load_path = "-", save_path = "-", unzip = False, file_type='.jpg'):
    if unzip:
       file_tools.zip_extract_all(load_path)
        
    dic = file_tools.path_dic(load_path)
    for folder_number in dic["folder_numbers"]:
        convert_all_in_folder(load_path, save_path, folder_number, file_type)
        
       
convert_all(load_path, save_path, unzip=True, file_type=".jpg")