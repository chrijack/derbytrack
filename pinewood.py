
from picamera import PiCamera
from time import sleep
from gpiozero import Button
# Doesn't work from omxplayer.player import OMXPlayer #TBD Unable to load OMXPlayer
# Doesn't work from omxplayer import OMXPlayer #TBD Unable to load OMXPlayer
# Doesn't work from omxplayer-wrapper import OMXPlayer #TBD Unable to load OMXPlayer
import os
from pathlib import Path

camera = PiCamera()
camera.rotation = 180 # Would perfer to rotate display so that cam is on top!

startbutton =Button(17)
stopbutton = Button(27)

VIDEO_PATH = Path("video.h264")
# TBD fixplayer = OMXPlayer(VIDEO_PATH)
RealTimeReplyLength = 3 # Play this many real time seconds in Slow Motion
# TBD fixplayer player = omxplayer(VIDEO_PATH)
SloMoFPS = 4
WaitAtFinish = 2

# TBD camera.start_preview() # USe this when program is working to see preview while recording, turned off now for debug

print ('Cam start up complete')
sleep(1)

print('top of prog')
while 1==1: # continuous loop to start video then reset based on starting gate from startbutton
        print ('Waiting for Start of race')
        if startbutton.is_pressed: # When race begins start recording video
                print ('Start Button pressed')
                print ('Cam ready to record')
                camera.start_recording('video.h264')
                print ('Cam is recording')
                while startbutton.is_pressed: #Loop until Startbutton is reset for new race
                        print ('Video recording')
                        if stopbutton.is_pressed: # When stop button is pressed stop rec and playback
                                print ('Stop Button Pressed')
                                print ('Waited ',WaitAtFinish,' seconds after first car - Time to stop recording')
                                camera.stop_recording() # Stop recording
                                print ('recording stopped')
                                sleep(1)
                                camera.stop_preview() # Disable preview
                                print ('Stopped Preview')


                                # Code to play last /SloMoFPS/ seconds of video in slow motion
                                # TBD FixPlayer SecondsInFile = player --audio_file video.h264 # TBD NOT WORKING get length of video
                                # TBD Above not working so set temp to 17
                                SecondsInFile = 17 # TBD remove when above fixed
                                print('Seconds in file determined to be = ', SecondsInFile)

                                # player  set start time to /SloMoFPS/ seconds less than length of clip
                                StartPosition = str(SecondsInFile - RealTimeReplyLength)
                                if len(StartPosition) == 1: # If start position is single digit, preceed with 0
                                    StartPosition = "0" + StartPosition
                                TimeString = '00:00:SS'
                                print(TimeString, 'before replace')
                                TimeString = TimeString.replace("SS",StartPosition)
                                print (TimeString + " is Timestring after replace" )
                                sleep(1)

                                # Loop Last SloMoFPS Seconds of Video
                                # player -b --loop --fps SloMoFPS -l --pos TimeString video.h264
                                # player -b --loop --fps SloMoFPS --display 5 -l --pos TimeString video.h264 #puts display out to HDMI
                                os.system("omxplayer video.h264 --loop --orientation 180 --fps 3") # Use os to run omx in shell but can't seem to stop it same way.

                                # WHEN RESET IS HIT Stop Video Play and/or Return to top of program
                                while startbutton.is_pressed:
                                        print ('Slo Mo Playing')
                                # player.stop #TBD need code to stop omxplayer replay
                                os.system("omxplayer video.h264 -i") #TBD this doesn't seem to be working but can't tell for sure without loop working
                        print ('End of while code') 

