pulseaudio --check
pulseaudio -D

python3 sound_test.py

python3 Camera_1.py &
python3 Camera_2.py 

kill %1