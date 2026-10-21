import simpleaudio as sa
import simpleaudio.functionchecks as fc
import time

def test():
    
    time.sleep(0.01)
    fc.LeftRightCheck.run()
    time.sleep(0.01)
    

def help():

    time.sleep(0.01)
    wave_obj = sa.WaveObject.from_wave_file("/home/.../Desktop/help_please.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()
    