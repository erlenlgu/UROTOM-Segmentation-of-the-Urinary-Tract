%% MULTIPLE DICOMs
%% Specify location and name of files
fileFolder = "D:\OneDrive - NTNU\Documents TUL\DICOM\DICOM files\series-000001";
files = dir(fullfile(fileFolder,'*.dcm'));
fileNames = {files.name}';

%% Info from the first file
info = dicominfo(fullfile(fileFolder,fileNames(1)));

%% Extract size info from metadata (not used) (from first file only)
voxel_size = [info.PixelSpacing; info.SliceThickness]';

%% Read first file to get size
I = dicomread(fullfile(fileFolder,fileNames(1))); % Reading one image
classI = class(I); % Class type of the image
sizeI = size(I); % Image dimensions
numImages = length(fileNames); % Number of DICOM images in series

%% Array of DICOM images
hWaitBar = waitbar(0,'Reading DICOM files');

ct = zeros(sizeI(1),sizeI(2),numImages,classI);

for i = length(fileNames):-1:1
    fname = fullfile(fileFolder,fileNames(i));
    ct(:,:,i) = uint16(dicomread(fname));
    
    waitbar((length(fileNames)-i+1)/length(fileNames));
end

delete(hWaitBar);

%% Showing DICOM images (one by one)
ct_rev = flipdim(ct, 3); % Reversing the order (not used)

figure(1);
for i = 100 : 150
    imshow(ct(:,:,i),{});
end

%% Adjust individual images (copy to Command Window)
% imtool(ct(:,:,200),{})

%% Thresholding one image
imNum = 180;
ctTemp = ct(:,:,imNum);

figure(2);
subplot(1,3,1); imshow(ctTemp,{}); title("Original");

lb = 1000; ub = 1150; % Found using histogram in imtool
ctTemp(ctTemp <= lb) = 0; % Ignore softer tissues
ctTemp(ctTemp >= ub) = 0; % Ignore harder tissues

subplot(1,3,2); imshow(ctTemp,{}); title("Thresholded");

ctTemp = imadjust(ctTemp);
%imfill(ctTemp,"holes");
subplot(1,3,3); imshow(ctTemp,{}); title("Adjusted");

%% Montage of every 20th slice
figure(3);
montage(ct(:,:,1:20:361),"DisplayRange",{});

%% Montage of every 20th slice (with thresholding)
ctThr = ct;
lb = 900; ub = 1200; % Found using histogram in imtool
ctThr(ctThr <= lb) = 0; % Ignore softer tissues
ctThr(ctThr >= ub) = 0; % Ignore harder tissues

figure(4);
montage(ctThr(:,:,1:20:361),"DisplayRange",{});

%% Play using imshow3D
figure(5);
imshow3D(ct);

%% Play using imshow3D (with thresholding)
figure(6);
imshow3D(ctThr);
