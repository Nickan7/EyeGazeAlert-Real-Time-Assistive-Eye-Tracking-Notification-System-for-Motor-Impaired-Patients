
import cv2
import numpy as np
from math import hypot



def get_gaze_ratio(eye_points, facial_landmarks, frame, gray):

	eye_region = np.array([ 
		(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
		(facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
		(facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
		(facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
		(facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
		(facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)])
		
	
	height,width,_ = frame.shape
	mask = np.zeros((height,width))
	cv2.polylines(mask, [eye_region], True, 255, 2)
	cv2.fillPoly(mask, [eye_region], 255)
	eye = cv2.bitwise_and(gray,gray,mask)

	min_x = np.min(eye_region[:,0])
	max_x = np.max(eye_region[:,0])
	min_y = np.min(eye_region[:,1])
	max_y = np.max(eye_region[:,1])
   

	gray_eye = eye[min_y: max_y, min_x: max_x]
	_, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
	height, width = threshold_eye.shape

	left_side_threshold = threshold_eye[0:height, 0: int(width/2)]
	left_side_white = cv2.countNonZero(left_side_threshold)

	right_side_threshold = threshold_eye[0:height, int(width/2) : width]
	right_side_white = cv2.countNonZero(right_side_threshold)


	if left_side_white==0:

		gaze_ratio=0

	elif right_side_white==0:

		gaze_ratio=0

	else:

		gaze_ratio = left_side_white / right_side_white

	return gaze_ratio
