import pydicom as dicom

# Choose an image to process
dcm = dicom.dcmread('./Sample Images/img.dcm')

#%% Showing data in the file set
print(dcm)

#%% Keys: print(dir(ds))
print(dir(dcm))

#%% Manufacturer (key)
dcm.Manufacturer

# Manufacturer (tag)
dcm[0x0008, 0x0070].value

# Manufacturer Model Name (key)
dcm.ManufacturerModelName

# Manufacturer Model Name (tag)
dcm[0x0008,0x1090].value

#%% Patient information
dcm.dir("pat")

# Gender of patient
dcm.PatientSex

#%% Changing the values
dcm.PatientID = "12345"
dcm.SeriesNumber = 5
dcm[0x10,0x10].value = 'Test'
