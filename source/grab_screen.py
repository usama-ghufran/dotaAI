from PIL import ImageGrab
import numpy as np
import cv2

MINIMAP_SCREEN_X_MIN = 9
MINIMAP_SCREEN_X_MAX = 270
MINIMAP_SCREEN_Y_MIN = 809
MINIMAP_SCREEN_Y_MAX = 1070


def get_minimap_coordinates(x_min, x_max, y_min, y_max):

    window_name = "SET_MINIMAP_COORDINATES"
    window_size = 600
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, window_size, window_size)
    while(True):
        img = ImageGrab.grab( bbox=(x_min,
                                    y_min,
                                    x_max,
                                    y_max)
                            )
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        cv2.imshow(window_name, frame)
        k = cv2.waitKey(1)
        if k == ord('q') or k == 27:
            cv2.destroyAllWindows()
            break
        
        elif k == ord('1'):
            x_min-=1
        elif k == ord('!'):
            x_min+=1
        
        elif k == ord('2'):
            x_max-=1
        elif k == ord('@'):
            x_max+=1
        
        elif k == ord('3'):
            y_min-=1
        elif k == ord('#'):
            y_min+=1
        
        elif k == ord('4'):
            y_max-=1
        elif k == ord('$'):
            y_max+=1

        elif k == ord('s'):
            print(" X_MIN: {}\n X_MAX: {}\n Y_MIN: {}\n Y_MAX: {}\n".format(x_min, x_max, y_min, y_max))

        elif k == ord('g'):
            cv2.imwrite("capture.png",frame)

get_minimap_coordinates(x_min=MINIMAP_SCREEN_X_MIN, x_max=MINIMAP_SCREEN_X_MAX,
                        y_min=MINIMAP_SCREEN_Y_MIN, y_max=MINIMAP_SCREEN_Y_MAX)