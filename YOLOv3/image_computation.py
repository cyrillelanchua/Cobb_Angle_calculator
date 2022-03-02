import numpy as np
import math
import cv2
#function to classify the cobb angle
def classify(angle,location):
    #angle[0] = top    angle[1] = bot
    angle[0] = abs(angle[0])
    angle[1] = abs(angle[1])
    if angle[1]>10 or angle[0]>10:
    
        if angle[1]>10 and angle[0]>10:
           print("pass")
           if location[1] != location[0]:
               result = "Combined Scoliosis"
           else:
               result = "Thoraco-Lumbar Scoliosis"
            
        else:
            if angle[0]>angle[1]:
                result = "Thoracic Scoliosis"
            else:
                result = "Lumbar Scoliosis"

    else:
        result = "No scoliosis"
        
    return result

#func to get the center of the rectangle
def getCenter(x1,y1,x2,y2):
    midx = (x1+x2)/2
    midy = (y1+y2)/2
    return int(midx), int(midy)

#gets two points then draws the line into the image
# used to create the lines for the tangent lines
def placelines(x,y,x2,y2,img):
    poly = np.polyfit([x,x2],[y,y2],1)
    function = np.poly1d(poly)
    img = cv2.line(img,(0,int(truncate(np.polyval(function,0)))),
                         (img.shape[0],int(truncate(np.polyval(function,img.shape[0])))),(0,0,255),4)
    # returns the min xy and max xy
    #[ymin,xmin,ymax,xmax]
    return [0, int(truncate(np.polyval(function,0))), img.shape[1], int(truncate(np.polyval(function,img.shape[1])))]
    
#function to get the closest number from the roots
def getClosest(num,array):
    diff = []
    for value in array:
        diff.append(abs(num-value))
    return diff.index(min(diff))

#remove decimals
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier


def deriv(f,x):

    h = 0.000000001                 #step-size 
    return (f(x+h) - f(x))/h        #definition of derivative



#get the slope of a line  
def getSlope(x1,y1,x2,y2):
    if (x2-x1) == 0:
        return 0
    else:
        return (y2-y1)/(x2-x1)

def getAngle(s1, s2): 
    return math.degrees(math.atan((s2-s1)/(1+(s2*s1))))

#gets the intersection of two lines
def lineIntersection(xline1,yline1, xline2,yline2):
    xdiff = (xline1[0] - xline1[len(xline1)-1], xline2[0] - xline2[len(xline2)-1])
    ydiff = (yline1[0] - yline1[len(yline1)-1], yline2[0] - yline2[len(yline2)-1])

    def det(x, y):
        return x[0] * y[len(y)-1] - x[len(x)-1] * y[0]

    div = det(xdiff, ydiff)
    if div == 0:
       print('lines do not intersect')
       return 0, 0, False

    d = (det(xline1,yline1), det(xline2,yline2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y, True #outputs the coordinates of the point of intersection

#Function to rotate the points of the bounding rectangle so that it is parallel to the line
#rotates the point around the center of the rectangle
def rotatePoints(xc,yc,x,y,w,h,angle,angleLower):
    x0 = ((x - xc) * math.cos(angle)) - ((y - yc) * math.sin(angle)) + xc;
    y0 = ((x - xc) * math.sin(angle)) + ((y - yc) * math.cos(angle)) + yc;
    
    x1 = (((x+w) - xc) * math.cos(angle)) - ((y - yc) * math.sin(angle)) + xc;
    y1 = (((x+w) - xc) * math.sin(angle)) + ((y - yc) * math.cos(angle)) + yc;
    
    x2 = ((x - xc) * math.cos(angleLower)) - (((y+h) - yc) * math.sin(angleLower)) + xc;
    y2 = ((x - xc) * math.sin(angleLower)) + (((y+h) - yc) * math.cos(angleLower)) + yc;
    
    x3 = (((x+w) - xc) * math.cos(angleLower)) - (((y+h) - yc) * math.sin(angleLower)) + xc;
    y3 = (((x+w) - xc) * math.sin(angleLower)) + (((y+h) - yc) * math.cos(angleLower)) + yc;
    return (x0,y0,x1,y1,x2,y2,x3,y3)

def calculateRoots(midListy, midListx):
    fit = np.polyfit(midListy, midListx, 5) #compute for the curve using curve fitting
    function = np.poly1d(fit)  #this is to get the function of the curve
    points = np.linspace(min(midListy), max(midListy), 100) #declare 100 point between the lower and upper bound of the midListy
    deriv = function.deriv()   #Derivative of the function
    deriv2 = deriv.deriv()    #Second Derivative of the function
    roots = np.roots(deriv2) #Get the roots of the second derivative
    return function, points, roots
