%% ONE DICOM
%% Read image
image = dicomread("D:\OneDrive - NTNU\Documents TUL\DICOM\DICOM files\1-12.dcm");

%% Read info
info = dicominfo("D:\OneDrive - NTNU\Documents TUL\DICOM\DICOM files\1-12.dcm");

%% Show
figure(1); imshow(file,{});
title("1-12");