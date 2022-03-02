import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import traceback
from image_computation import *



def computeCobb(img):
# Load Yolo
    try:
     net = cv2.dnn.readNet( "yolov3_testing.cfg","yolov3_training_last.weights")

# Name custom object
     classes = ["vertebrae"]
     layer_names = net.getLayerNames()
     output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
     colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Loading image
     img = cv2.resize(img, None, fx=0.4, fy=0.4)
     height, width, channels = img.shape
     imgResult = img.copy()
    # Detecting objects
     blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
     net.setInput(blob)
     outs = net.forward(output_layers)

    # Showing informations on the screen
     class_ids = []
     confidences = []
     boxes = []
    except Exception:
     traceback.print_exc()
    for out in outs:
        
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)



    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    
    font = cv2.FONT_HERSHEY_PLAIN
    #declare a list for the midpoint coordinates of each detected vertebrae
    midListx=[]
    midListy=[]
    boxCoordinates = []
    #this is to check if there is no detected vertebrae
    if len(boxes)==0:
        return (None,None)

    
    #Get the center of each rectangle
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            
            color = colors[class_ids[i]]

            #place the rectangle and vertebrae text   
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 2)
            #get the center of each rectangle
            midx, midy = getCenter(x,y,(x + w),(y + h))
            #Put X coordinate of the center into a List
            midListx.append(midx)
            #Put Y coordinate of the center into a List
            midListy.append(midy)
            #Draw a dot at the center of each rectangle
            cv2.rectangle(img, (midx,midy) ,(midx+1,midy+1)  , color, 2)
            
            #Coordinates for the box
            boxCoordinates.append([midx,midy,x,y,w,h])
                 
   
    function, points, roots = calculateRoots(midListy, midListx)



    ######################## angle calculation#########################
    try:
     
     #sorts the array based on value of midy
     boxCoordinates = sorted(boxCoordinates, key=lambda x: x[1])

     midListySorted= sorted(midListy)
     index = []
     rootsSorted = sorted(roots)
     
     #gets the index of the roots/inflection point in midListySorted
     index.append(getClosest(rootsSorted[0],midListySorted))
     color = (0, 255, 0)
     cv2.rectangle(img, (boxCoordinates[index[0]][0],midListySorted[index[0]]) ,(boxCoordinates[index[0]][0]+1,midListySorted[index[0]]+1)  , color, 2)

     index.append(getClosest(rootsSorted[1],midListySorted)+1)

     cv2.rectangle(img, (boxCoordinates[index[1]][0],midListySorted[index[1]]) ,(boxCoordinates[index[1]][0]+1,midListySorted[index[1]]+1)  , color, 2)
    
     if midListySorted[getClosest(rootsSorted[2],midListySorted)]>rootsSorted[2]:
        index.append(getClosest(rootsSorted[2],midListySorted)-1)
     else:
        index.append(getClosest(rootsSorted[2],midListySorted))
     cv2.rectangle(img, (boxCoordinates[index[2]][0],midListySorted[index[2]]) ,(boxCoordinates[index[2]][0]+1,midListySorted[index[2]]+1)  , color, 2)
     

     
     slope = [] #slope of each vertebrae
     angle = []

     coorRotated = []
     angleTan =[]
     slopeTan= []#slope of the tangent lines

     ctr=0
     #tangent lines coordinates
     tanLinCoor = []
     #tangent line ymin/ymax and xmin/xmax
     xlineCoor = []
     ylineCoor = []
     for i in range(len(boxCoordinates)):
     #coorCenter.append([midx,midy,x,y,w,h])
         
          #Gets the slope of the middle point of the first and second
         if i==0:#start iteration
            slope.append(getSlope(boxCoordinates[i][0],boxCoordinates[i][1],boxCoordinates[i+1][0],boxCoordinates[i+1][1]))

         elif i== (len(boxCoordinates)-1):#ending iteration
            slope.append(getSlope(boxCoordinates[i][0],boxCoordinates[i][1],boxCoordinates[i-1][0],boxCoordinates[i-1][1]))
         else:
            slope.append(getSlope(boxCoordinates[i-1][0],boxCoordinates[i-1][1],boxCoordinates[i+1][0],boxCoordinates[i+1][1]))
         
         #obtained the coordinate and slope at the computed indexes
         if (ctr!=3) and (index[ctr] == i) : #ctr!=3 to stop the checking

            if i==0:
               tanLinCoor.append(placelines(boxCoordinates[i][0],boxCoordinates[i][1],boxCoordinates[i+1][0],boxCoordinates[i+1][1],imgResult))
            elif i== (len(boxCoordinates)-1):
               tanLinCoor.append(placelines(boxCoordinates[i][0],boxCoordinates[i][1],boxCoordinates[i-1][0],boxCoordinates[i-1][1],imgResult))
            else:
               tanLinCoor.append(placelines(boxCoordinates[i-1][0],boxCoordinates[i-1][1],boxCoordinates[i+1][0],boxCoordinates[i+1][1],imgResult))
            if slope[i] == 0:
                slopeTan.append(999)
                xlineCoor.append(np.linspace(tanLinCoor[ctr][0], tanLinCoor[ctr][2], 100))
                ylineCoor.append(np.linspace(tanLinCoor[ctr][1], tanLinCoor[ctr][3], 100))
                ctr = ctr+1
            else:
                slopeTan.append(slope[i])
             #get the intesection of two tangent lines 
                xlineCoor.append(np.linspace(tanLinCoor[ctr][0], tanLinCoor[ctr][2], 100))
                ylineCoor.append(np.linspace(tanLinCoor[ctr][1], tanLinCoor[ctr][3], 100))
                ctr = ctr+1

         #to compare where the angle is positive, zero or negative    
         if getAngle(0,slope[i])>0:
            angle.append(90-getAngle(0,slope[i]))
         elif getAngle(0,slope[i])==0:
            angle.append(0)             
         else:
            angle.append(-(getAngle(0,slope[i])+90))
         
         #places the function into the imgResult
         if i != (len(boxCoordinates)-1):
            cv2.line(imgResult,(boxCoordinates[i][0],boxCoordinates[i][1]),(boxCoordinates[i+1][0],boxCoordinates[i+1][1]),(0,0,255),3)
         
         #rotatePoints(xc,yc,x,y,w,h,angle,angleLower)
         coorRotated.append( rotatePoints(boxCoordinates[i][0],boxCoordinates[i][1],
                                boxCoordinates[i][2],boxCoordinates[i][3],
                                boxCoordinates[i][4],boxCoordinates[i][5],
                                (-angle[i]*(math.pi/180)),(-angle[i]*(math.pi/180))))
         #draws the rotated boxes into the image
         cv2.line(imgResult,(int(truncate(coorRotated[i][0])),int(truncate(coorRotated[i][1]))),(int(truncate(coorRotated[i][2])),int(truncate(coorRotated[i][3]))),(0,255,0),1)
         cv2.line(imgResult,(int(truncate(coorRotated[i][4])),int(truncate(coorRotated[i][5]))),(int(truncate(coorRotated[i][6])),int(truncate(coorRotated[i][7]))),(0,255,0),1)
         cv2.line(imgResult,(int(truncate(coorRotated[i][0])),int(truncate(coorRotated[i][1]))),(int(truncate(coorRotated[i][4])),int(truncate(coorRotated[i][5]))),(0,255,0),1)
         cv2.line(imgResult,(int(truncate(coorRotated[i][2])),int(truncate(coorRotated[i][3]))),(int(truncate(coorRotated[i][6])),int(truncate(coorRotated[i][7]))),(0,255,0),1)
     
     #contains the coordinates for the intersections of tangent lines
     tanInter = []
 
     for i in range(len(xlineCoor)-1):
        tanInter.append(lineIntersection(xlineCoor[i],ylineCoor[i],xlineCoor[1+i],ylineCoor[1+i]))

     
     #contains the location of the intersection whether left or right
     location = []

     for i in range(len(tanInter)):
        if tanInter[i][0] < img.shape[1]/2 :
            location.append("Left")
        else:
            location.append("right")

    #contains the angle of the tangent lines which is equal to the upper and lower angle
     for i in range(len(slopeTan)-1):
        angleTan.append(getAngle(slopeTan[i],slopeTan[1+i]))
     #places the angle into the image 
        cv2.putText(imgResult, str(truncate(abs(angleTan[i]),2)), (int(tanInter[i][0]),int(tanInter[i][1])), font, 3, (0,0,255), 2)
    #for cases where only one angle is computed
     if len(angleTan) == 1 :
        angleTan.append(angleTan[0])
        location.append(location[0])
     classResult = classify(angleTan, location)

    except Exception:
     traceback.print_exc()

    ######################### angle calculation#########################

    #########################Plotting###################################
    #initialize the plot to show the images
    fig, (ax1,ax2,ax3) = plt.subplots(1,3,sharex=True, sharey=True, figsize=(10,10))
    #shows the detected vertebrea
    ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    #makes ax2 size equal to ax1 and ax3
    ax2 .set_aspect('equal')
    ax2.axis([0,img.shape[1] , img.shape[0],0])

    #plots the points in the middle plot
    ax2.plot(midListx,midListy,'ro')

    #plots the line in the middle plot
    ax2.plot( function(points),points)
    #show the 3rd image in the plot
    ax3.imshow(cv2.cvtColor(imgResult, cv2.COLOR_BGR2RGB))
    #########################Plotting###################################
    return (angleTan[0], angleTan[1], imgResult, classResult)

