import cv2



def get_dims(cap, res):

    STD_DIMENSIONS = {
    "480p" : (640, 480),
    "720p" : (1280, 720),
    "1080p" : (1920, 1080),
    "4k" : (3840, 2160),
    }


    width, height = STD_DIMENSIONS[res]
    
    cap.set(3, width)
    cap.set(4, height)

    return width, height