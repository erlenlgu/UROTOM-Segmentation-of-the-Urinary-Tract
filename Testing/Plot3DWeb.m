%% 3D plot from web... slow
figure(99);

k = 180 : 190;
N = isosurface(ct(:,:,k));
p = patch(N);
isonormals(ct(:,:,k),p);
cdata = smooth3(rand(size(ct(:,:,k))),"box",7);
isocolors(cdata,p);
p.FaceColor = [.75 .75 .75];
p.EdgeColor = "none";
camlight
grid on