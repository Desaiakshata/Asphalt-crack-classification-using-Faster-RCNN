import numpy as np
from object_detection.utils import np_box_list
from object_detection.utils import np_box_list_ops
from object_detection.utils import np_box_ops


def wheelpath(marking_list):
    '''
    Creates arrays for different sections of the pavement using the values from the markings.xls file
    '''
    left_wheelpath = np.array(([0,marking_list[0],1250.0,marking_list[1]]))
    right_wheelpath = np.array(([0,marking_list[2],1250.0,marking_list[3]]))
    non_wheelpath = np.array(([0,marking_list[1],1250.0,marking_list[2]]))
    left_center_path = np.array(([0,marking_list[0]-100,1250.0,marking_list[2]]))
    right_center_path = np.array(([0,marking_list[1],1250.0,marking_list[3]+100]))
    left_non_wheelpath = np.array(([0,marking_list[4],1250.0,marking_list[0]]))
    right_non_wheelpath = np.array(([0,marking_list[3],1250.0,marking_list[5]]))
    return left_wheelpath, right_wheelpath, non_wheelpath, left_center_path, right_center_path, left_non_wheelpath,right_non_wheelpath 


def cracks(boxes,classes,scores,marking_list):
    left_wheelpath,right_wheelpath,non_wheelpath,left_center_path, right_center_path, left_non_wheelpath,right_non_wheelpath = wheelpath(marking_list)
    
    right_center_list_b2 = []
    left_center_list_b2 = []
    left_center_list_b3 = []
    right_center_list_b3 = []
    right_list_b = []
    left_list_b = []
    center_b = list()
    right_list_l = []
    left_list_l = []
    box_list_right_load = []
    box_list_left_load = []
    b1_box_list = list()
    b1_box_list_longi = list()
    b1_class_list = list()
    box_list_block = list()
    rm_list = list()
    flag_LC3 =0
    flag_BC2 = 0
    flag_BC3 = 0
    box_left = np_box_list.BoxList(np.array(([left_wheelpath])))
    box_right = np_box_list.BoxList(np.array(([right_wheelpath])))
    box_non_wheel = np_box_list.BoxList(np.array(([non_wheelpath])))
    box_left_center = np_box_list.BoxList(np.array(([left_center_path])))
    box_right_center = np_box_list.BoxList(np.array(([right_center_path])))
    box_non_wheel_left = np_box_list.BoxList(np.array(([left_non_wheelpath])))
    box_non_wheel_right = np_box_list.BoxList(np.array(([right_non_wheelpath])))
    
    for i in range(boxes.shape[0]):
        label = classes[i]
        box = boxes[i]
        box2 = np_box_list.BoxList(np.array(([box])))
        print('box2',box2)
        
        #Check for box overlaps with wheepaths and non-wheelpaths
        ioa_1 = np.transpose(np_box_list_ops.ioa(box_non_wheel, box2)) #non-wheelpath
        ioa_2 = np.transpose(np_box_list_ops.ioa(box_left, box2))      #Left wheelpath
        ioa_3 = np.transpose(np_box_list_ops.ioa(box_right, box2))     #Right wheelpath
        ioa_4 = np.transpose(np_box_list_ops.ioa(box_left_center, box2))     #Left center path
        ioa_5 = np.transpose(np_box_list_ops.ioa(box_right_center, box2))     #Right center path
        ioa_7 = np.transpose(np_box_list_ops.ioa(box_non_wheel_left, box2))     #Left nonwheelpath
        ioa_8 = np.transpose(np_box_list_ops.ioa(box_non_wheel_right, box2))     #Right nonwheelpath


        if classes[i]==3:
          ioa_6 = np.transpose(np_box_list_ops.ioa(box2,box_non_wheel)) #LC3
          if ioa_6>0.8:
            flag_LC3 =1
        if 3 not in classes:
          flag_LC3 =1
          
        
        #Check detected load cracks in the non wheelpath and change the label to BC1
        if (ioa_1 > 0.8 or ioa_7 > 0.7) or ioa_8 > 0.7:
            if label in [1,2,3,4]:
                classes[i] = 5
                
        #creating a list of BC1 boxes and classes    
        if (classes[i] == 6 or classes[i] == 5):
          if classes[i]==5:
            b1_box_list.append(boxes[i])
            b1_class_list.append(classes[i])


          #Calculate the area of the bbox
          area = np_box_ops.area(np.array(([box]))) 

          # appending the BC2/BC3 detections to left,right and center lists of the pavement dependig on their location and area.
          if classes[i] == 6:
            if ioa_4 > 0.7:
                if area > 190000:
                    left_center_list_b2.append(classes[i])
                    #left_center_list_b2
                    box_list_block.append(boxes[i])

                else:
                    left_center_list_b3.append(classes[i])
                    #left_center_list_b3
                    box_list_block.append(boxes[i])

            elif ioa_5 > 0.7:
                if area > 190000:
                    right_center_list_b2.append(classes[i])
                    box_list_block.append(boxes[i])
                    #right_center_list_b2

                else:
                    right_center_list_b3.append(classes[i])
                    #right_center_list_b3
                    box_list_block.append(boxes[i])


            #To check if the biggest box is in the center of the image
            if ((ioa_4 > 0.5 and ioa_5 > 0.5) or (area > 400000)):
                if area>200000:
                    if ioa_7 > 0.2 or ioa_8 > 0.2:
                        center_b.append(classes[i])


        #Check for load cracks        
        else:
            #left_wheelpath
            if ioa_2 > 0.4:
                if classes[i] !=3:
                    left_list_l.append(classes[i])
                    box_list_left_load.append(boxes[i])

            #right_wheelpath
            elif ioa_3 > 0.4:
                if classes[i] !=3:
                    right_list_l.append(classes[i])
                    box_list_right_load.append(boxes[i])

            #special case LC3 with not much overlap because of wide box
            if classes[i]==3:
                if ioa_2 > 0.3:
                    left_list_l.append(classes[i])
                    box_list_left_load.append(boxes[i])
                if ioa_3 > 0.3:
                    right_list_l.append(classes[i])
                    box_list_right_load.append(boxes[i])
                    
                
            
    
    #Part of the code to post-process BC2/BC3 into BC2 and BC3 separately

    #check if LC4 is not present in detections
    if np.setdiff1d(classes,[1,2,3,5,6]).shape[0] ==0:
        if flag_LC3==1:


          #Checking if the nuumber of detected boxes is greater than 3
          if (len(left_center_list_b2+left_center_list_b3+right_center_list_b2+right_center_list_b3)) >= 4:
            if (len(left_center_list_b2+left_center_list_b3)>=1 and len(right_center_list_b2+right_center_list_b3)>=1):
                print('Block crack level 3 detected')
                flag_BC3 = 1
            else:
                print('Block crack level 2 detected')
                flag_BC2 = 1


          #check if BC2 is detected wrt area of the detected box being bigger than BC3
          elif ((len(left_center_list_b2)!=0) or (len(right_center_list_b2)!=0)):
            if len(center_b)>=1:
                print('Block crack level 2 detected')
                flag_BC2 = 1

            #Checking if the nuumber of detected boxes is greater than or equal to 2
            elif (len(left_center_list_b2+left_center_list_b3+right_center_list_b2+right_center_list_b3)) >= 2:

                #Check if blocks are detected in both left and right parts of the pavement
                if (len(left_center_list_b2+left_center_list_b3)>=1 and len(right_center_list_b2+right_center_list_b3)>=1):
                    print('Block crack level 3 detected')
                    flag_BC3 = 1
                else:
                    print('Block crack level 2 detected')
                    flag_BC2 = 1

            elif (len(left_center_list_b2+left_center_list_b3+right_center_list_b2+right_center_list_b3)) >= 1:
                print('Block crack level 2 detected')
                flag_BC2 = 1

          #Check for blocks detected only in one part of the pavement (R or L) >= 2
          elif len(left_center_list_b2+left_center_list_b3) >=2 or len(right_center_list_b2+right_center_list_b3) >= 2:
            #if 6 in classes:
            flag_BC2 = 1
            print('Block Crack Level 2 detected')

    # Part of the code to return crack extent calculation
    if not (flag_BC2 or flag_BC3):
      extent_right,extent_left,extent_b1 = extent(box_list_right_load,box_list_left_load,box_list_block,b1_box_list,flag_BC2,flag_BC3)
      
      left_list_l.sort()
      left_list_l.reverse()
      right_list_l.sort()
      right_list_l.reverse()
      
      
      if (left_list_l==[] and right_list_l==[]) :
        if extent_b1!=0:      
          return('0',extent_left,'0',extent_right,0,0,'1',extent_b1)
        else:
          return('0',extent_left,'0',extent_right,0,0,0,0)
      elif left_list_l==[]:
        if len(right_list_l)>=2:
          right = str(right_list_l[0]) + ',' + str(right_list_l[1])
        else:
          right = str(right_list_l[0])
        if extent_b1!=0:
          return(0,extent_left,right,extent_right,0,0,'1',extent_b1)
        else:
          return(0,extent_left,right,extent_right,0,0,0,0)
      elif right_list_l==[]:
        if len(left_list_l)>=2:
          left = str(left_list_l[0]) + ',' + str(left_list_l[1])
        else:
          left = str(left_list_l[0])
        if extent_b1!=0:
          return(left,extent_left,0,extent_right,0,0,'1',extent_b1)
        else:
          return(left,extent_left,0,extent_right,0,0,0,0)
      else:
        if len(left_list_l)>=2:
          left = str(left_list_l[0]) + ',' + str(left_list_l[1])
        else:
          left = str(left_list_l[0])
        if len(right_list_l)>=2:
          right = str(right_list_l[0]) + ',' + str(right_list_l[1])
        else:
          right = str(right_list_l[0])
        if extent_b1!=0:
          return(left,extent_left,right,extent_right,0,0,'1',extent_b1)
        else:
          return(left,extent_left,right,extent_right,0,0,0,0)
    else:
      extent_block,extent_right, extent_left = extent(box_list_right_load,box_list_left_load,box_list_block,b1_box_list,flag_BC2,flag_BC3)
      
      left_list_l.sort()
      left_list_l.reverse()
      right_list_l.sort()
      right_list_l.reverse()
      if (left_list_l==[] and right_list_l==[]) :
          left = '0'
          right = '0'
      elif left_list_l==[]:
          left = '0'
          if len(right_list_l)>=2:
            right = str(right_list_l[0]) + ',' + str(right_list_l[1])
          else:
            right = str(right_list_l[0])
      elif right_list_l ==[]:
          right = '0'
          if len(left_list_l)>=2:
            left = str(left_list_l[0]) + ',' + str(left_list_l[1])
          else:
            left = str(left_list_l[0])
      else:
        if len(left_list_l)>=2:
          left = str(left_list_l[0]) + ',' + str(left_list_l[1])
        else:
          left = str(left_list_l[0])
        if len(right_list_l)>=2:
          right = str(right_list_l[0]) + ',' + str(right_list_l[1])
        else:
          right = str(right_list_l[0])
      if flag_BC2:
        return (left,extent_left,right,extent_right,'2',str(extent_block),'0','0')
      else:
        return (left,extent_left,right,extent_right,'3',str(extent_block),'0','0')

def extent(box_list_right_load,box_list_left_load,box_list_block,b1_box_list,flag_BC2,flag_BC3):
  '''
  Calculates the load cracking and block cracking extents for entire pavement section.
  Returns the crack extent values.
  '''

  length_right=length_left=length_center=0
  length_block = 0
  length_b1 = 0
  intersect_h_l = 0
  intersect_h_r = 0
  #intersect_h_c = 0
  list_r =[]
  list_l=[]
  #list_c=[]

  def intersect_height(list_1,list_2):
      '''
      Function to calculate the intersecting length between boxes. This length is required to
      be subtracted from the calculated crack extent.
      '''
      intersect_h = 0
      for i in range(len(list_1)):
          for j in range(len(list_1)):
              if i != j:
                  b=[i,j]
                  b.sort()
                  if (b not in list_2):
                    intersect_h += intersecting_height(list_1[i],list_1[j])
                    a=[i,j]
                    a.sort()
                    list_2.append(a)
      return intersect_h,list_2 
                  
  intersect_h_l,list_l = intersect_height(box_list_left_load,list_l)
  intersect_h_r,list_r = intersect_height(box_list_right_load,list_r)
  #intersect_h_c,list_c = intersect_height(box_list_center_load,list_c)
  
  length_left -=intersect_h_l
  length_right -=intersect_h_r
  #length_center -=intersect_h_c

  def box_length(box_list):
      length = 0
      for i in box_list:
          length += i[2]-i[0]
      if length > 1000:
          length = 5000
      else:
          length = length * 4
      return length

    
  # If BC2/BC3 cracks are not detected 
  if not (flag_BC2 or flag_BC3):
    for i in b1_box_list:
        if (i[3]-i[1]) > (i[2]-i[0]):
            length_b1+=(i[3]-i[1])*4
        else:
            length_b1+=(i[2]-i[0])*4
        
    # Extent right and left wheelpath
    length_right = box_length(box_list_right_load)
    length_left = box_length(box_list_left_load)
    
    
    return length_right,length_left,length_b1    

  else:
    #LC extent calculation to match the updated GDOT Protocol (Taking into account Sam's response)
    length_right = box_length(box_list_right_load)
    length_left = box_length(box_list_left_load)
    
    #BC2/BC3 extent calculation
    for i in b1_box_list:
        if (i[3]-i[1]) > (i[2]-i[0]):
            length_block+=(i[3]-i[1])*4
        else:
            length_block+=(i[2]-i[0])*4
    
    for i in box_list_block:   
        length_block+=(2*(i[2]-i[0]) + 2*(i[3]-i[1]))*4

    return length_block, length_right, length_left
    
def remove_b1(boxes,classes,scores,marking_list):
    '''
    This function eliminates all BC1 cracks that are part of BC2/BC3.
    Longitudinal cracks that are in the non-wheelpath and are part of BC2/BC3 are also deleted.
    It returns the undeleted boxes, classes and scores
    '''

    left_wheelpath,right_wheelpath,non_wheelpath,left_center_path, right_center_path, left_non_wheelpath,right_non_wheelpath = wheelpath(marking_list)
    box_left = np_box_list.BoxList(np.array(([left_wheelpath])))
    box_right = np_box_list.BoxList(np.array(([right_wheelpath])))
    box_non_wheel_left = np_box_list.BoxList(np.array(([left_non_wheelpath])))
    box_non_wheel_right = np_box_list.BoxList(np.array(([right_non_wheelpath])))
    box_non_wheel = np_box_list.BoxList(np.array(([non_wheelpath])))

    rm_list = list()
    b1_box_list = list()
    b1_class_list = list()
    box_list_block = list()


    for i in range(boxes.shape[0]):
        box = boxes[i]
        label=classes[i]
        box2 = np_box_list.BoxList(np.array(([box])))
        ioa_1 = np.transpose(np_box_list_ops.ioa(box_non_wheel, box2))           #non-wheelpath
        ioa_7 = np.transpose(np_box_list_ops.ioa(box_non_wheel_left, box2))      #Left nonwheelpath
        ioa_8 = np.transpose(np_box_list_ops.ioa(box_non_wheel_right, box2))     #Right nonwheelpath

        #All LC cracks in the three non-wheelpath zones are changed to class BC1 == 5
        if (ioa_1 > 0.8 or ioa_7 > 0.7) or ioa_8 > 0.7:
                if label in [1,2,3,4]:
                    classes[i] = 5

    #Creating lists for BC1 and BC2/BC3 cracks
    for i in range(boxes.shape[0]):
        if classes[i] == 5:
            b1_box_list.append(boxes[i])
            b1_class_list.append(classes[i])
        elif classes[i] == 6:
            box_list_block.append(boxes[i])
                
    #Eliminating all BC1 cracks that are part of BC2/BC3                                
    for i in range(len(b1_box_list)):
      if len(b1_box_list)!=0 and len(box_list_block)!=0:
        for j in range(len(box_list_block)):
            b1 = np_box_list.BoxList(np.array(([b1_box_list[i]])))
            b2 = np_box_list.BoxList(np.array(([box_list_block[j]])))

            ioa_2 = np.transpose(np_box_list_ops.ioa(box_left, b1))      #Left wheelpath
            ioa_3 = np.transpose(np_box_list_ops.ioa(box_right, b1))     #Right wheelpath
            ioa_check_b1 = np.transpose(np_box_list_ops.ioa(b2, b1))
            b1_length = abs(b1_box_list[i][2]-b1_box_list[i][0])
            b1_width = abs(b1_box_list[i][3]-b1_box_list[i][1])
            
            if b1_length > b1_width:
                if ioa_check_b1 > 0.2:
                    if not (ioa_2 > 0.3 or ioa_3 > 0.3):
                        print('------------------------',np.where(boxes==b1_box_list[i])[0])

                        if len(np.where(boxes==b1_box_list[i])[0])!=0:
                         rm_list.append(np.where(boxes==b1_box_list[i])[0][0])
            else:
                if ioa_check_b1 > 0.5:
                  if len(np.where(boxes==b1_box_list[i])[0])!=0:
                    rm_list.append(np.where(boxes==b1_box_list[i])[0][0])
                      
        boxes = np.delete(boxes,rm_list, 0)
        classes = np.delete(classes,rm_list,0)
        scores = np.delete(scores,rm_list, 0)
    return boxes,classes,scores

   
def remove_overlaps(boxes,classes,scores,marking_list):
    '''
    This function deletes the overlapping boxes that belong to the same crack class.
    It returns the boxes, classes and scores of the un-deleted (non-overlapping) boxes.
    '''
    boxes,classes,scores = remove_b1(boxes,classes,scores,marking_list)
    
    k = boxes.shape[0]
    boxes_=boxes
    remove_list =[]
    for i in range(k):
        if classes[i] == 6: #not deleting the BC2/BC3 detections as they do not have overlaps
              continue
        for j in range(k):
            if classes[j] == 6:
              continue
            area1 = np_box_ops.area(np.array(([boxes_[j]]))) 
            area2 = np_box_ops.area(np.array(([boxes_[i]]))) 
            box1 = np_box_list.BoxList(np.array(([boxes_[j]])))
            box2 = np_box_list.BoxList(np.array(([boxes_[i]])))
            ioa1 = np.transpose(np_box_list_ops.ioa(box1, box2))
            ioa2 = np.transpose(np_box_list_ops.ioa(box2, box1))

            #A minimum overlap threshold to consider the overlapping boxes that need to be deleted
            if ioa1 > 0.65:
              #To check if its not the same detected box
              if ioa1 < 0.99:
                if classes[i] not in [5,6]:
                    #A check for overlaps using the ioa scores wrt (box1 , box2) and vice versa.
                    #This is to delete the box with most overlap
                    if abs(ioa1 - ioa2) <= 0.01:
                      if ioa1 > ioa2:
                        if i not in remove_list:
                          if classes[i] == classes[j]:
                            remove_list.append(i)
                      else:
                        if j not in remove_list:
                          if classes[i] == classes[j]:
                            remove_list.append(j)
                    else:
                      if classes[i] == classes[j]:
                        remove_list.append(i)
                if classes[i] == classes[j]== 5:
                    remove_list.append(i)
              elif ioa1 >= 0.99:
                if area1 != area2:
                  if classes[i] == classes[j]:
                    remove_list.append(i)

    
    boxes = np.delete(boxes,remove_list, 0)
    classes = np.delete(classes,remove_list,0)
    scores = np.delete(scores,remove_list,0)
    return boxes, classes, scores
                  
def intersecting_height(box1,box2):
    '''
    This function calculates the overlaps between two LC detections in the same wheelpath so that
    the overlapping height can be subtracted during extent calculations. It returns the calculated
    intersecting heights
    '''
    [y_min1, x_min1, y_max1, x_max1] = [box1[0],box1[1],box1[2],box1[3]]
    [y_min2, x_min2, y_max2, x_max2] = [box2[0],box2[1],box2[2],box2[3]]
    all_pairs_min_ymax = np.minimum(y_max1, np.transpose(y_max2))
    all_pairs_max_ymin = np.maximum(y_min1, np.transpose(y_min2))
    intersecting_heights = np.maximum(np.zeros(all_pairs_max_ymin.shape),all_pairs_min_ymax - all_pairs_max_ymin)
    return intersecting_heights
        
                
                
                
            
        
