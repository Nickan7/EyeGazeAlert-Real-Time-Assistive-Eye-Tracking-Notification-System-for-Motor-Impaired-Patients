import wiringpi as wpi
import time



def blink(color):
    
	wpi.digitalWrite(color, 1)
	time.sleep(0.5)
	wpi.digitalWrite(color, 0)
	time.sleep(0.5) 


def on(color):
	wpi.digitalWrite(color, 1)


def off(color):
	wpi.digitalWrite(color, 0)



def test(green_color,blue_color,red_color):
    wpi.wiringPiSetup()
    wpi.pinMode(green_color, 1)
    wpi.pinMode(blue_color, 1)
    wpi.pinMode(red_color, 1)


    wpi.digitalWrite(green_color, 1)
    time.sleep(0.5)
    wpi.digitalWrite(green_color, 0)
    time.sleep(0.5)

    wpi.digitalWrite(blue_color, 1)
    time.sleep(0.5)
    wpi.digitalWrite(blue_color, 0)
    time.sleep(0.5)

    wpi.digitalWrite(red_color, 1)
    time.sleep(0.5)
    wpi.digitalWrite(red_color, 0)
    time.sleep(0.5)    