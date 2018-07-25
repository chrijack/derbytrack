import sys
import io
import picamera
import RPi.GPIO as GPIO
import time
import os
from subprocess import Popen
import pygame.display
import pygame.event

#Set up confirguration
isoVal = 0
expmode = 'sports'
postseconds = 1.0
totalseconds = 1.5
thisframerate = 90
playbackframerate = 15
theoplaytime = totalseconds * thisframerate / playbackframerate
firstsleep = theoplaytime + 1
secsleep = firstsleep + 5

#set blank screen behind everything
pygame.display.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill((0, 0, 0))

#set up GPIO using BCM Numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
camera = picamera.PiCamera()
camera.vflip = True
camera.hflip = True
camera.resolution = (640, 480)
camera.framerate = thisframerate
camera.exposure_mode = 'sports'
camera.iso = isoVal
stream = picamera.PiCameraCircularIO(camera, seconds=7)
camera.start_recording(stream, format='h264', intra_period = 10)
videocount = 1

#set up directory for files
dirpref = time.strftime("%b%d%y")
directory = dirpref + "/"
dircreated = False
dirsuf = 0
while not dircreated:
    if os.path.exists(directory):
        #add suffix and check again
        dirsuf = dirsuf + 1
        directory = dirpref + "/" + str(dirsuf) + "/"
    else:
        #create directory
        os.makedirs(directory)
        dircreated = True
camera.start_preview()
running = True
try:
    while running:
        for event in pygame.event.get():
            if (event.type == pygame.KEYUP and event.key == pygame.K_c and
                event.mod & pygame.KMOD_CTRL):
                pygame.quit()
                sys.exit()
        camera.wait_recording(0.2)
        if GPIO.input(5) == False:
            camera.wait_recording(postseconds)
            filemp4 = directory + "race" + str(videocount) + ".mp4"
            filename = directory + "race" + str(videocount) + ".h264"
            stream.copy_to(filename, seconds=totalseconds)
            convertstring = "MP4Box -fps " + str(playbackframerate) + " -add " + filename + " " + filemp4
            #playerstring = "omxplayer " + filemp4
            os.system(convertstring)
            #os.system(playerstring)
            omxc = Popen(['omxplayer', filemp4])
            camera.stop_preview()
            time.sleep(firstsleep)
            omxc = Popen(['omxplayer', filemp4])
            videocount = videocount + 1

            time.sleep(secsleep)
            camera.start_preview()

finally:
    pygame.display.quit()
    GPIO.cleanup()
    camera.stop_recording()
    camera.stop_preview()
    camera.close()
    sys.exit()
