import numpy as np
import cv2


img_path = "enemy.png"
window_name = "sprite"





def trackbar_callback(pos):
    # Do nothing
    pass


def main():

	img = cv2.imread(img_path,0)
	
	cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
	cv2.namedWindow("masked", cv2.WINDOW_NORMAL)
	cv2.createTrackbar('thresh', window_name, 0, 255, trackbar_callback)
	
	while(True):
		pos = cv2.getTrackbarPos('thresh',window_name)
		ret,thresh = cv2.threshold(img,pos,255,cv2.THRESH_BINARY)
		masked = cv2.bitwise_and(img,img,mask = thresh)
		cv2.imshow(window_name,thresh)
		cv2.imshow("masked",masked)
		
		k = cv2.waitKey(1)
		if k == 27:         # wait for ESC key to exit
		    cv2.destroyAllWindows()
		    break
		elif k == ord('s'): # wait for 's' key to save and exit
		    cv2.imwrite("mask_"+img_path,masked)
	    

main()