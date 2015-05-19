clear
close all
clc

% Set resolution
res=512;  
development = true

% Path of the images
% img_folder='C:\train';
img_folder='/home/morten/Git_and_dropbox_not_friends/Retina/sample';

mkdir(fullfile(img_folder,['outimages' sprintf('%i',res)]))

%% Get images in the folder
fl = dir(fullfile(img_folder,'*.jpeg')); 
% load('dirlist')

% fl(cc).name = '29984_left.jpeg'; cc=cc+1;
% fl(cc).name = '35058_left.jpeg'; cc=cc+1;
if development 
    fl = fl(4);
end
%% Loop for the images
% parpool(4);
doplot = false; 

parfor ii=1:length(fl);
    
    
    %% Get the image
    fprintf('%s. Processing %i of %i\n',fl(ii).name, ii,length(fl));
    A = imread(fullfile(img_folder,fl(ii).name));
    
    if size(A,1)>size(A,2) % 15840_left.jpeg in the test set is wrongly rotated
        A=rot90(A);
    end
    
    %% Remove noise from the black background
    ma = mean(A,3); ma = ma / max(ma(:));
    v = ma(round(end/4:end*3/4),round(end/4:end*3/4));
    median(v(:));
    ma = ma / median(v(:));
    
    if false && doplot,
        
        subplot(2,1,1);     
        B = mean(A,3) > 30; 
        imshow(B)

        subplot(2,1,2);    
        B = ma > 30/250; 
        imshow(B)
    end
    ma = uint8(ma > 30/250);
    
    %% Remove small connected components
    cc = bwconncomp(ma); 
    for j=1:length(cc.PixelIdxList)
        lp = cc.PixelIdxList{j};
        if length(lp) < 100, 
            ma(lp) = 0;
        end
    end
    
    %% Detect edges in the image
    B = edge(mean(bsxfun(@times, A, ma)  ,3),'canny');
    if doplot,
        imshow(A)
    end
    [h,w] = size(B);
    
    %% Find outer edges in the eye and fit a circle to these

    pcirc = zeros(0,2);
    for i=1:h,
        mv1 = find(B(i,1:round(end/2)),1,'first');
        mv2 = w/2+find(B(i,round(w/2):end),1,'last');

        if isempty(mv1) || isempty(mv2), continue; end
        pcirc(end+1,:) = [mv1,i];
        pcirc(end+1,:) = [mv2,i];

    end
    [cx,cy,cr] = circfit(pcirc(:,1),pcirc(:,2));
    if doplot, 
        subplot(1,1,1);
        imshow(A); hold on;
        plot(cx,cy,'ro');
        plot(pcirc(:,1),pcirc(:,2),'b.');
        th = linspace(0,2*pi);
        plot(cx+ cos(th)*cr,cy + sin(th)*cr,'g-');
    end 

    %% find the radius of the circle
    % compute the distance to the radius.
    rs = sqrt(sum(bsxfun(@minus,pcirc,[cx,cy]).^2,2));
    if doplot,
        plot(cx+ cos(th)*cr*0.95,cy + sin(th)*cr*0.95,'g:');
    end
    
    %% Remove points inside the circle and refine the fit
    Iinside = rs < cr * 0.95;
    if ~isempty(Iinside),
    %     pcirc = pcirc(Iinside,:);
         plot(pcirc(Iinside,1),pcirc(Iinside,2),'yo');
    end

    pcirc = pcirc(~Iinside,:);
    [cx,cy,cr] = circfit(pcirc(:,1),pcirc(:,2));

    % subplot(2,2,2);
    % hist(rs)
    I = rs > cr  * 1.015;
    if doplot,
        plot(cx+ cos(th)*cr*1.015,cy + sin(th)*cr*1.015,'m:');
    end
    
    %% Count number of points outside the fitted circle, to see if the image is inverted or not
    % subplot(2,2,1)
    % plot(pcirc(I,2),pcirc(I,1),'ro');
    if nnz(I) > 20, 
        if doplot, title('THIS GUY IS INVERTED','FontSize',20,'FontWeight','Bold'); 
        %%
        mc = median(pcirc(I,:),1);

        plot(mc(1),mc(2),'gx'); hold on;
    %     J = sqrt(sum(bsxfun(@minus, pcirc, mc).^2,2)) < cr * 0.08;

    %     plot(pcirc(I & J,1),pcirc(I & J,2),'m.');
    %     plot(mc(1),mc(2),'gx'); hold on;
        end
        %%
        image_is_inverted = false;
    else
        image_is_inverted = true;
    end 
    
    %% Zero padding in the y direction if needed
    cy = round(cy);
    cx = round(cx);
    cr = floor(cr);
    pady1 = -min(0,round(cy - cr))+2;
    pady2 = max(0,round(cy + cr - size(A,1)))+2;
    A = cat(1,zeros(pady1,size(A,2),size(A,3)), A,zeros(pady2,size(A,2),size(A,3)));
    cy = cy + pady1;

    minx = max(1,cx -cr); maxx = min(size(A,2),cx+cr);
    miny = max(1,cy -cr); maxy = min(size(A,1),cy+cr);

    %% Get subimage of the eye and resize it
    da = A(miny:maxy, minx:maxx,:);
    As = imresize(da, [res, res]);
    
    %% Rotate/Invert images
    ss = fl(ii).name;
    is_left = strcmp(ss(find(ss == '_')+1:find(ss == '.')-1),'left');
    if image_is_inverted,
    %     As = As(:,end:-1:1,:);
        As = rot90(As);
        As = rot90(As);
    end  
    if is_left, 
        As = As(:,end:-1:1,:);
    end 

    %% Save final result in png format
    imwrite(As,fullfile(img_folder,['outimages' sprintf('%i',res) '/',fl(ii).name(1:end-5),'.png']));
  
end