
import cv2
import dlib
import numpy as np
from math import hypot
import wiringpi as wpi
import time
import simpleaudio

import variables as var
import led
import dimensions as dims
import blink
import gaze
import sound


back_or_side = var.back_or_side

cap = cv2.VideoCapture(var.camera_2) 

cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))

width, height = dims.get_dims(cap, res="480p")


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/home/nikotini/Desktop/shape_predictor_81_face_landmarks.dat")
font = cv2.FONT_HERSHEY_PLAIN

counter_frames = 0
times_blinking = 0

right_eye = var.right_eye
left_eye = var.left_eye

warning_bound_of_frames_for_Alert = var.warning_bound_of_frames_for_Alert
bound_of_frames_for_Alert = var.bound_of_frames_for_Alert
bound_of_blinkings_for_Help = var.bound_of_blinkings_for_Help
number_of_demicals_accuracy_of_gaze_ratio_both_eyes = var.number_of_demicals_accuracy_of_gaze_ratio_both_eyes
 
green_color = var.green_color_1
blue_color = var.blue_color_1
red_color = var.red_color_1


led.test(green_color,blue_color,red_color)


while True:

	_, frame = cap.read()

	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
	
	faces = detector(gray)
	


	for face in faces:
	   

		landmarks = predictor(gray, face)
		

		# Blinking and Gaze Detection

		if back_or_side == 0 :

			blinking_ratio = blink.get_blinking_ratio(left_eye, landmarks, frame)
			gaze_ratio_both_eyes = round(   gaze.get_gaze_ratio(left_eye, landmarks, frame, gray)   , number_of_demicals_accuracy_of_gaze_ratio_both_eyes)
			height_of_closed_eyes = var.height_of_closed_eyes_back
			deviation_from_direct = var.deviation_from_direct_back

		else:

			blinking_ratio = blink.get_blinking_ratio(right_eye, landmarks, frame)
			gaze_ratio_both_eyes = round(   gaze.get_gaze_ratio(right_eye, landmarks, frame, gray)    , number_of_demicals_accuracy_of_gaze_ratio_both_eyes)
			height_of_closed_eyes = var.height_of_closed_eyes_side
			deviation_from_direct = var.deviation_from_direct_side




		# Extra counters
		cv2.putText(frame, "Gaze Ratio " + str(gaze_ratio_both_eyes), (50,140), font, 2, (0,255,0), 3)
		cv2.putText(frame, "Counter Frames " + str(counter_frames), (50,180), font, 2, (0,0,255), 3)
		cv2.putText(frame, "Times Blinking " + str(times_blinking), (50,220), font, 2, (255, 0, 0), 3)
		cv2.putText(frame, "Blinking Ratio " + str( round(blinking_ratio, number_of_demicals_accuracy_of_gaze_ratio_both_eyes) ), (50,260), font, 2, (255, 0, 0), 3)
		cv2.line(frame, ( int(width/2), 0)   ,  (int(width/2), height ), (0,255,255),1)
		cv2.line(frame, (0 , int(height/2) ), ( int(width), int(height/2) ), (0,255,255),1)
			


		# Requirements for Katerina and Alert
		if gaze_ratio_both_eyes > 1 + deviation_from_direct :
			
			# Ideal Position
			counter_frames+=1
			cv2.putText(frame, "Ideal", (100,450), font, 10, (0,255,0), 7)
			led.on(green_color)


				
			# Warning Alert
			if counter_frames==warning_bound_of_frames_for_Alert:
				
				# Red Led Blink
				led.blink(red_color)
		

		
			# Alert
			elif counter_frames==bound_of_frames_for_Alert:

				counter_frames=0
				cv2.putText(frame, "ALERT !!!", (100,100), font, 7, (0, 0, 255), 10 )
				sound.help()
							    

             

		    # If see around make the counter zero for the next blinkings
			if blinking_ratio > height_of_closed_eyes:
				
				counter_frames=0
				times_blinking+=1

 
				
				# Warning help announcement
				if times_blinking==bound_of_blinkings_for_Help-1:
				
					#Blue Led
					led.blink(blue_color)

                # Help annoucement
				elif times_blinking==bound_of_blinkings_for_Help:
				   
					counter_frames=0
					times_blinking=0
					cv2.putText(frame, "HELP !!!", (100,100), font, 7, (255, 0, 0), 10 )
					sound.help()


		else:	

			cv2.putText(frame, "NOT Ideal", (30,450), font, 7, (255,0,255), 7)
			counter_frames=0
			times_blinking=0
			led.off(green_color)


	# Plots

	cv2.imshow("Right Camera",frame)


	key = cv2.waitKey(1)
	
	if key == 27:
	   break

led.off(green_color)
led.off(red_color)
led.off(blue_color)

cap.release()
cv2.destroyAllWindows()