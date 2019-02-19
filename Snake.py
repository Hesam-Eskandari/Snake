
from cv2 import waitKey
from cv2 import destroyAllWindows
from cv2 import imshow
from cv2 import line
from cv2 import circle
from cv2 import putText
from cv2 import FONT_HERSHEY_SIMPLEX
from cv2 import LINE_AA
from cv2 import VideoWriter
from cv2 import resize
from cv2 import imread
from numpy import shape
from numpy import array
from numpy import ones
from random import randint

def square(ground,x_center,y_center,edge,thick,fill,color=[0,0,0]):
    """
    #points defined as numpy array
    points = array([[x_center-int(edge/2.0+0.5),y_center-int(edge/2.0+0.5)],
                    [x_center+int(edge/2.0+0.5),y_center-int(edge/2.0+0.5)],
                    [x_center+int(edge/2.0+0.5),y_center+int(edge/2.0+0.5)],
                    [x_center-int(edge/2.0+0.5),y_center+int(edge/2.0+0.5)]])
    """
    if edge > 0:
        #points defined as a list of lists
        points = [[x_center-int(edge/2.0+0.5),y_center-int(edge/2.0+0.5)],
                  [x_center+int(edge/2.0+0.5),y_center-int(edge/2.0+0.5)],
                  [x_center+int(edge/2.0+0.5),y_center+int(edge/2.0+0.5)],
                  [x_center-int(edge/2.0+0.5),y_center+int(edge/2.0+0.5)]]
        #print points
        #print shape(ground)
        for ind in [-1,0,1,2]:
            #drow lines give points in a list
            line(ground,(points[ind][0],points[ind][1]),(points[ind+1][0],points[ind+1][1]),color,thick)
            #drow lines give points in a numpy array
            #line(ground,(points[ind,0],points[ind,1]),(points[ind+1,0],points[ind+1,1]),color,thick)
        if fill == False:
            return ground
        return square(ground,x_center,y_center,edge-thick*1.9,thick,fill,color)
    else:
        return ground
    

dim_y = 500
dim_x = int(dim_y*1.618+0.5)
out = VideoWriter('snake.mp4',4, 60, (dim_x,dim_y))
ground = ones((dim_y,dim_x,3))*255
ground = ground.astype('uint8')
edge, margin = 400, 20
x_center, y_center = 550, 250
ground = square(ground,x_center,y_center,edge,10,False,[255,0,0])
edge_s = 20
x_head,y_head = [randint(-8,8)*edge_s+x_center, randint(-8,8)*edge_s+y_center]
centers = [[x_head,y_head]]
thick = 2
food = [randint(-8,8)*edge_s+x_center, randint(-8,8)*edge_s+y_center]
square(ground,food[0],food[1],edge_s-2,thick,True,[55,155,155])
j=0
v_x = 20
v_y = 0
speed = 2
length = len(centers)
putText(ground,'Speed: '+str(speed),(30,120),FONT_HERSHEY_SIMPLEX, 1.0, (100, 100, 10), lineType= LINE_AA)
while True:
    if speed == length/6:
        speed+=1
        ground[95:125,145:190] = 255
        putText(ground,'Speed: '+str(speed),(30,120),FONT_HERSHEY_SIMPLEX, 1.0, (100, 100, 10*+speed*3), lineType= LINE_AA)
        
    j+=1
    length = len(centers)
    ground[22:57,160:230]=255
    putText(ground,'Length: '+str(length),(30,50),FONT_HERSHEY_SIMPLEX, 1.0, (80, 80, 80), lineType= LINE_AA)
    ground[57:92,215:280]=255
    putText(ground,'Remaining: '+str(361-length),(30,85),FONT_HERSHEY_SIMPLEX, 1.0, (80, 80, 250-length/2), lineType= LINE_AA)
    imshow('Snake',ground)
    i = 1
    if food == centers[-1]:
        key = waitKey(20-length/24) & 0xFF
        while True:
            i+=1
            food = [randint(-9,9)*edge_s+x_center, randint(-9,9)*edge_s+y_center]
            if ground[food[1]-5,food[0]-5,0] != 0:
                square(ground,food[0],food[1],edge_s-2,thick,True,[55,155,155])
                break
            elif i>=5000:
                key = ord('q')
                break
    else:
        key = waitKey(100-length/6) & 0xFF
    if len(centers) == 361:
        putText(ground,'You Win',(250,250),FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), lineType= LINE_AA)
    if v_x+v_y!=0:
        centers.append([centers[-1][0]+v_x,centers[-1][1]+v_y])
        if ground[centers[-1][1]-5,centers[-1][0]-5,0]==0:
            print 'you lose'
            record = 0
            while record < 60:
                record +=1
                putText(ground,'Game Over',(250,250),FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), lineType= LINE_AA)
                imshow('Snake',ground)
                out.write(ground)
                waitKey(1)
            break
    if food != centers[-1] and v_x+v_y!=0:
        square(ground,centers[0][0],centers[0][1],edge_s-2,thick,True,[255,255,255])
        centers.remove(centers[0])
        imshow('Snake',ground)
        
    else:
        pass
        
    for i in centers:
        square(ground,i[0],i[1],edge_s-2,thick,True,[0,0,0])
    if (centers[-1][0] > 720 or 380 >centers[-1][0]) and v_y==0:
        v_x, a = 0, 1
    if (centers[-1][1] > 420 or 80 >centers[-1][1]) and v_x==0:
        v_y, a = 0, 1
    if key == 27 or length == 360:
        break
    elif key == ord('q'):
        waitKey(0)
        break
    elif key == ord('w') and v_y == 0 and 80 < centers[-1][1]:
        v_x, v_y, a = 0, -20, 0
    elif key == ord('s') and v_y == 0 and centers[-1][1] < 420:
        v_x, v_y, a = 0, 20, 0
    elif key == ord('d') and v_x == 0 and centers[-1][0] < 720:
        v_x, v_y, a = 20, 0, 0
    elif key == ord('a') and v_x == 0 and 380 < centers[-1][0]:
        v_x, v_y,a = -20, 0, 0
    out.write(ground)
# winner scenario: from here to end
ground[:,:,:] = 255
edge, margin = 400, 20
x_center, y_center = 550, 250
ground = square(ground,x_center,y_center,edge,10,False,[255,0,0])
#length = 360
if length ==360:
    for column in range(19):
        for row in range(19):
            fill_ground = [(column-9)*edge_s+x_center, (row-9)*edge_s+y_center]
            #circle(ground,(fill_ground[0],fill_ground[1]),5,[0,0,0],4)
            square(ground,fill_ground[0],fill_ground[1],edge_s-2,thick,True,[0,0,0])
            imshow('Snake',ground)
            out.write(ground)
            key = waitKey(1) & 0xFF
            if key == 27:
                break
    record = 0      
    while record < 10:
        record+= 1
        out.write(ground)
        imshow('Snake',ground)
        waitKey(1)
    pose = [-9*edge_s+x_center,-9*edge_s+y_center]
    w_x, w_y = edge_s, 0
    box = [720,420,380,80]
    color = [255,255,255]
    start = 0
    while True:
        square(ground,pose[0],pose[1],edge_s-2,thick,True,color)
        if pose[0] > box[0] and pose[1] < box[1] and w_x!=0:
            w_x, w_y = 0, edge_s
            box[3]+= edge_s
        elif pose[0] > box[0] and pose[1] > box[1] and w_y!=0:
            w_x, w_y = -1*edge_s, 0
            box[0]-= edge_s
        elif pose[0] < box[2] and pose[1] > box[3] and w_x!=0:
            w_x, w_y = 0, -1*edge_s
            box[1]-= edge_s
        elif pose[0] < box[2] and pose[1] < box[3] and w_y!=0:
            w_x, w_y= edge_s, 0
            box[2]+= edge_s
            start += 1
            #ground = square(ground,x_center,y_center,edge,10,False,[255,255,255])
            #ground = square(ground,x_center,y_center,edge-edge_s*2,10,False,[255,0,0])
            #edge -=2*edge_s
        elif pose == [x_center,y_center]:
            break        
        if start >= 1:
            ground = square(ground,x_center,y_center,edge,10,False,[255,255,255])
            edge -=(start)**1.4/5.0
            ground = square(ground,x_center,y_center,edge,10,False,[255,0,0])

        pose = [pose[0]+w_x,pose[1]+w_y]
        imshow('Snake',ground)
        out.write(ground)

        key = waitKey(10) & 0xFF
        if key == 27:
            break
    waitKey(300)
    t=0
    image = imread('farnaz1.jpg')
    #imshow('image',image)
    #waitKey(0)
    print shape(image)
    edge=2
    while True:
        t+=1
        ground[:,:,:]=255
        if t < 50:
            putText(ground,'You Win',(290,250),FONT_HERSHEY_SIMPLEX, 2.0, (220, 120, 120),2)
        elif t < 100:
            putText(ground,'Here\'s A Gift',(210,250),FONT_HERSHEY_SIMPLEX, 2.0, (220, 120, 120),2)
        else:
            x,y = shape(image)[0],shape(image)[1]
            edge +=2
            template = resize(image,(edge,int(edge*x/y)/2*2))
            try:
                ground[y_center-int(edge*x/y)/2:y_center+int(edge*x/y)/2,404-edge/2:404+edge/2] = template
            except:
                break
        imshow('Snake',ground)
        out.write(ground)
        key = waitKey(20) & 0xFF
        if key == 27:
            break
    
waitKey(0)
out.release()
destroyAllWindows()