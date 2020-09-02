import cv2
import numpy as np
from matplotlib import pyplot as plt
import xml.etree.ElementTree as ET
import os
import xlwt 
from xlwt import Workbook 
import xlrd
from xlutils.copy import copy
import argparse

def main():
    '''
    This file can be used to draw lane markings as well as the wheelpath boundaries on the image.
    It also saves the location of all these boundaries in the markings.xls file which is saved in the
    images folder and can be used for post-processing
    '''
 
    parser = argparse.ArgumentParser(description='draws the lane markings and wheelpath boundaries on an image')
    parser.add_argument("--image_path", type=str, default = '/home/a1/Custom-Faster-RCNN/dataset/Images/', help = 'path for training images')
    parser.add_argument("--xml_path", type=str, default = '/home/a1/Custom-Faster-RCNN/dataset/xml/', help = 'provide the path for lcms xml files')
    parser.add_argument("--save_path", type=str, default = '/home/a1/Custom-Faster-RCNN/dataset/Images/', help = 'provide the path to save the images')

    args = parser.parse_args()   
    image_dir = args.image_path
    xml_dir = args.xml_path
    save_dir = args.save_path
    
    Max_Left_Lane = 1285
    Min_Right_Lane = 2873
    wb = Workbook() 
    file_list = os.listdir(image_dir)
    sheet1 = wb.add_sheet('Sheet 1')
    j = 0
    for filename in file_list:
        
        img_path = image_dir + filename[:-4] + ".jpg"
        print(img_path)
        img = cv2.imread(img_path,1)
        file_name = xml_dir + filename[0:11] + filename[20:-4] + '.xml'
        tree = ET.parse(file_name)
        root = tree.getroot()
        for child in root:
            if child.tag=='LaneMarkInformation':
                a = float(root[5][2][1].text) 
                b = float(root[5][3][1].text)  

                if a == 5:
                    center = b - 2*914.4;
                else:
                    if b == 4155:
                        center = a + 2*914.4;
                    else:
                        center = (a + b) / 2;
                Left_Boundary = b - Min_Right_Lane
                Right_Boundary = a + 4160 - Max_Left_Lane

                #Calculating wheelpath boundaries
                l_s = (max(Left_Boundary, center - 457.2 - 930))/4  #(center - 457.2 - 930)/4 
                l_e = (center - 457.2)/4
                r_s = (center + 457.2)/4
                r_e = (min(Right_Boundary, center + 457.2 + 930))/4 #(center + 457.2 + 930)/4 

                #Left and right lane markings
                a = a/4
                b = b/4
                #print(center,a,b)
        
        #drawing lane-markings
        cv2.line(img,(int(a)-35,0),(int(a)-35,1250),(255,255,255),10) #(255,0,0)
        cv2.line(img,(int(b)+35,0),(int(b)+35,1250),(255,255,255),10) #(255,0,0)
        #cv2.line(img,(0,625),(1040,625),(255,255,255),1) #(255,0,0) -- can be used as reference for annotation

        #masking
        #cv2.rectangle(img,(0,1250),(int(a),0),(128,128,128),-1)
        #cv2.rectangle(img,(int(b),1250),(1040,0),(128,128,128),-1)

        
        list_lines = [l_s, l_e, r_s, r_e]
        m=0
        headings = ['img','l_s','l_e','r_s','r_e','l_lane_mark','r_lane_mark']
        for i in range(len(headings)):
            if j!=0:
                break
            sheet1.write(j,i,headings[i])   
        j+=1
        sheet1.write(j, m, filename)

        #drawing wheelpath boundaries
        for i in list_lines:
                 sheet1.write(j, m+1, i)
                 m+=1
                 cv2.line(img,(int(i),0),(int(i),1250),(0,0,255),1, cv2.LINE_AA)

        sheet1.write(j,m+1,a)
        sheet1.write(j,m+2,b)
        savepath = save_dir + filename[:-4] + '.jpg' 
        cv2.imwrite(savepath, img)

    wb_save = save_dir + 'markings.xls'
    wb.save(wb_save)


if __name__ == "__main__":
    main()
