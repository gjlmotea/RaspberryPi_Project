import os
import glob
import subprocess
import RPi.GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
btn_next = 16
btn_prev = 20
btn_stop = 19
btn_pause = 25

GPIO.setup(btn_next, GPIO.IN)
GPIO.setup(btn_prev, GPIO.IN)
GPIO.setup(btn_stop, GPIO.IN)
GPIO.setup(btn_pause, GPIO.IN)
sleep(1)

path = '/home/pi/songs'

f = [op.path.join(dirpath, fn)
     for dirpath, dirnames, files in os.walk(path)
     for fn in files if fn.endswith('.mp3')
    ]

print(f)

h = len(f)

flag = 1
pt = 0
st = 0

while(1):
    if flag == 1:
        player = subprocess.Popen(["omxplayer", f[pt]], stdin= subprocess.PIPE)
        fi = player.poll()
        flag = 0
        st = 0

    if GPIO.input(btn_next) == True:
        print("========== Next ==========")
        if st == 0:
            player.stdin.write("q")
        flag = 1
        pt = pt + 1
        if pt > h-1:
            pt = 0
        sleep(0.3)

    if GPIO.input(btn_prev) == True:
        print("========== Prev ==========")
        if st == 0:
            player.stdin.write("q")
        flag = 1
        pt = pt - 1
        if pt < 0:
            pt = h - 1
        sleep(0.5)

    if GPIO.input(btn_stop) == True:
        print("========== Stop ==========")
        sleep(0.3)
        fi = player.poll()
        if fi != 0:
            player.stdin.write("q")
            st = 1

    if GPIO.input(btn_pause) == True:
        sleep(0.3)
        fi = player.poll()

    if fi != 0:
        player.stdin.write("p")


    sleep(0.1)

        
