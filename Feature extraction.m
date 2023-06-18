clear,clc;
No_of_images=95;  %starting and ending point of the umages 

features=[;;;];
features1=[;;;];



for k=1:7     %here the final value of k depends on the number of files startng with A, B ,etc
    image= ['D:\NIRANJAN BITS FOLDER_BK_SG2_G(recent)\SEMESTER 5\COMP_PHY_CODES\Spectrograms - divided in A,B,C,D,EFGH\I',num2str(k,'%d'),'.png'];  %here we have considered summation of 7 png files starting with I
    Input=imread(image);
    gray=im2gray(Input)
    glcm=graycomatrix(gray)
    stats=graycoprops(glcm,'Contrast Correlation Energy Homogeneity');
    Contrast=stats.Contrast;
    Correlation=stats.Correlation;
    Energy=stats.Energy;
    Homogeneity=stats.Homogeneity;
    features1=[Contrast,Correlation,Energy,Homogeneity]
    features=vertcat(features,features1)
end    

csvwrite('features_informal_project.csv',features,k+1,4)  %k+1 just denotes the number of rows 


   %here variables are
   %1)ending value of k
   %2) the ending \A or\B or \I ,etc in the location of the image in line 10