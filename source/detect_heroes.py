import cv2
import numpy as np
from PIL import ImageGrab
#import threading


hero_window_name_prefix = "hero "
control_window_name = "CONTROLS"
minimap_window_name = "MINIMAP"
MINIMAP_SCREEN_X_MIN = 9
MINIMAP_SCREEN_X_MAX = 270
MINIMAP_SCREEN_Y_MIN = 809
MINIMAP_SCREEN_Y_MAX = 1070
x_pad = 350
y_pad = 350
x_offset = 500
COLUMNS = 4
radius = 7
pos = {}
ally_colour = (0,255,0)
enemy_colour = (0,0,255)
undecided_colour = (255,0,0)


HERO_KEY =  [
            # Hmin, Smin, Vmin, Hmax, Smax, Vmax
            [[107, 195,  75],  [112, 210,  255]],  # 0
            [[75,  150,  75],  [80,  165,  255]],  # 1
            [[146, 240,  75],  [151, 255,  255]],  # 2
            [[27,  230,  75],  [32,  255,  255]],  # 3
            [[11,  240,  75],  [16,  255,  255]],  # 4
            [[162, 115,  75],  [167, 130,  255]],  # 5
            [[33,  150,  75],  [38,  175,  255]],  # 6
            [[92,  150,  100],  [97,  165,  255]],  # 7
            [[64,  240,  50],  [70,  255,  255]],  # 8
            [[16,  240,  75],  [21,  255,  255]],  # 9
        
            ]
NUM_HEROES = 10

   

def create_channel(hsv, hkey=0):
    """Create a channel from the main image based on the colour key"""
    hero_window_name = hero_window_name_prefix+str(hkey)
    #cv2.namedWindow(hero_window_name, cv2.WINDOW_NORMAL)
    #cv2.moveWindow(hero_window_name, int(x_offset + x_pad*np.floor(hkey/(NUM_HEROES/COLUMNS))), int(y_pad*(hkey%(NUM_HEROES/COLUMNS))))

    col_min = np.array(HERO_KEY[hkey][0])
    col_max = np.array(HERO_KEY[hkey][1])
    channel = cv2.inRange(hsv, col_min, col_max)
    
    kernel_size = 3
    iterations = 1
    kernel = np.ones((kernel_size,kernel_size),np.uint8)
    channel = cv2.erode(channel,kernel, iterations = iterations)
    channel = cv2.dilate(channel,kernel, iterations = iterations)
    mask, contours, hierarchy = cv2.findContours(channel,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    bgr = cv2.bitwise_and(bgr,bgr,mask=channel)

    areas = []
    cx = -1
    cy = -1
    for c in contours:
        areas.append(cv2.contourArea(c))
    if areas:
        max_area = max(areas)
        if(max_area > 0):
            max_area_index = areas.index(max_area)
            
            M = cv2.moments(contours[max_area_index])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        
            #pos[hkey] = (cx, cy)
            #x,y,w,h = cv2.boundingRect(contours[max_area_index])
            #bgr = cv2.rectangle(bgr,(x,y),(x+w,y+h),(0,0,255),1)
            #bgr = cv2.circle(bgr,(cx,cy), radius, (0,0,255), 1)
        
        #cv2.drawContours(hsv, contours, -1, (255,0,0), 1)
    
    pos[hkey] = (cx, cy)
    #cv2.imshow(hero_window_name, bgr)


def trackbar_callback(pos):
    # Do nothing
    pass


def main():

    #minimap = cv2.imread("../data/hero_colours.png",cv2.IMREAD_COLOR)
    my_faction = -1
    window_size = 600
    cv2.namedWindow(minimap_window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(minimap_window_name, window_size, window_size)
    
    for i_hero in range(NUM_HEROES):
        pos[i_hero] = (-1, -1)

    while(True):
    
        mapgrab = ImageGrab.grab( bbox=(MINIMAP_SCREEN_X_MIN,
                                    MINIMAP_SCREEN_Y_MIN,
                                    MINIMAP_SCREEN_X_MAX,
                                    MINIMAP_SCREEN_Y_MAX)
                            )
        minimap = np.array(mapgrab)
        minimap = cv2.cvtColor(minimap, cv2.COLOR_BGR2RGB)
        
        hsv = cv2.cvtColor(minimap, cv2.COLOR_BGR2HSV)    
        for i_hero in range(NUM_HEROES):
            create_channel(hsv, i_hero)

        for i_hero in range(NUM_HEROES):
            cx, cy = pos[i_hero]
            if not (cx == -1 or cy == -1):
                if my_faction == -1:
                    cv2.circle(minimap, (cx, cy), radius, undecided_colour, 1)
                elif my_faction < 5:
                    if i_hero < 5:
                        cv2.circle(minimap, pos[i_hero], radius, ally_colour, 1)
                    else:
                        cv2.circle(minimap, pos[i_hero], radius, enemy_colour, 1)
                else:
                    if i_hero < 5:
                        cv2.circle(minimap, pos[i_hero], radius, enemy_colour, 1)
                    else:
                        cv2.circle(minimap, pos[i_hero], radius, ally_colour, 1)


        cv2.imshow(minimap_window_name, minimap)
        k = cv2.waitKey(1)
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()
            break
        elif k >= 48 and k <= 57:
            my_faction = k-48


def show_controls(hsv):

    cv2.namedWindow(control_window_name, cv2.WINDOW_NORMAL)
    cv2.createTrackbar('H min', control_window_name, 0, 255, trackbar_callback)
    cv2.createTrackbar('H max', control_window_name, 255, 255, trackbar_callback)
    cv2.createTrackbar('S min', control_window_name, 0, 255, trackbar_callback)
    cv2.createTrackbar('S max', control_window_name, 255, 255, trackbar_callback)
    cv2.createTrackbar('V min', control_window_name, 0, 255, trackbar_callback)
    cv2.createTrackbar('V max', control_window_name, 255, 255, trackbar_callback)
    cv2.imshow(control_window_name, minimap)
    cv2.moveWindow(control_window_name, 100, 100)

    while(True):
        h_min = cv2.getTrackbarPos('H min',control_window_name)
        h_max = cv2.getTrackbarPos('H max',control_window_name)
        s_min = cv2.getTrackbarPos('S min',control_window_name)
        s_max = cv2.getTrackbarPos('S max',control_window_name)
        v_min = cv2.getTrackbarPos('V min',control_window_name)
        v_max = cv2.getTrackbarPos('V max',control_window_name)

        col_min = np.array([h_min, s_min, v_min])
        col_max = np.array([h_max, s_max, v_max])

        channel = cv2.inRange(hsv, col_min, col_max)

        #create_channel(channel)

        cv2.imshow(hero_window_name_prefix, channel)
        
        k = cv2.waitKey(1)
        if k == 27:         # wait for ESC key to exit
            cv2.destroyAllWindows()
            break
        elif k == ord('s'): # wait for 's' key to save and exit
            print("H_min:"+str(h_min))
            print("H_max:"+str(h_max))
            print("S_min:"+str(s_min))
            print("S_max:"+str(s_max))
            print("V_min:"+str(v_min))
            print("V_max:"+str(v_max))
        



main()