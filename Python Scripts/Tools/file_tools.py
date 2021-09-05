"""
Written by Erlend L. Gundersen
    erlend.l.gundersen@gmail.com
"""

from zipfile import ZipFile
import os


# Extracting a given zip file
# input: folder_path: path to the folder where the .zip file is located
# input: zip_file_name: name of the .zip file that will be unzipped
def zip_extract(folder_path, zip_file_name):
    with ZipFile(os.path.join(folder_path,zip_file_name), 'r') as zip:
        print('Unzipping '+zip_file_name)
        zip.extractall(folder_path)


# Extracting all zip files in a given path
# input: folder_path: path to the folder where the .zip files are located
def zip_extract_all(folder_path):
    file_names_zip = [x for x in os.listdir(folder_path) if x.endswith(".zip")]
    for zip_file in file_names_zip:
        zip_extract(folder_path, zip_file)
    print('Done!')
    

# Dictionary of paths and names of folders and files in path
# input: path: path to a folder of zip files containing dicom files
# output: dictionary with information about the names and paths of folders and files
# in the given path
def path_dic(path):
    dic = {}
    dic["folder_names"] = [x for x in os.listdir(path) if os.path.isdir(os.path.join(path,x))]
    dic["folder_numbers"] = [i for i in range(len(dic["folder_names"]))]
    dic["folder_paths"] = [os.path.join(path, f) for f in dic["folder_names"]]
    dic["file_names"] = [os.listdir(p) for p in dic["folder_paths"]]
    
    file_paths = []
    for m in range(len(dic["folder_names"])):
        file_paths.append([os.path.join(dic["folder_paths"][m], f) for f in dic["file_names"][m]])
    dic["file_paths"] = file_paths
    return dic


# Creating a new folder if the folder does not exists in the path
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    