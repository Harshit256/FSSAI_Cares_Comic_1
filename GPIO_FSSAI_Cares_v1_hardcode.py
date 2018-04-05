from video_player import *
import RPi.GPIO as GPIO
import time
from time import sleep
import pygame
import sys

pygame.init()
infoObject = pygame.display.Info()
screen=pygame.display.set_mode((infoObject.current_w, infoObject.current_h),pygame.NOFRAME)

BASE_DIR = '/home/pi/Desktop/FSSAI_Cares/FSSAI_Care_Videos'
FILENAME_STORY_1 =  '/Comic_1/Scene_1.mp4'
FILENAME_STORY_2 =  '/Comic_2/Scene_1.mp4'
FILENAME_STORY_3 =  '/Comic_3/Scene_1.mp4'

play_path_video_story_1 = ''.join([BASE_DIR, FILENAME_STORY_1])
play_path_video_story_2 = ''.join([BASE_DIR, FILENAME_STORY_2])
play_path_video_story_3 = ''.join([BASE_DIR, FILENAME_STORY_3])

#play_story_1 = Player(play_path_video_story_1)
#play_story_2 = Player(play_path_video_story_2)
#play_story_3 = Player(play_path_video_story_3)

play_stories = []
play_stories.append(Player(play_path_video_story_1))
play_stories.append(Player(play_path_video_story_2))
play_stories.append(Player(play_path_video_story_3))

storyIndex = 2
oldStoryIndex = 1
image_path_1='/home/pi/Desktop/FSSAI_Cares/2018-03-24-142423_1360x768_scrot.png'
image_path_2='/home/pi/Desktop/FSSAI_Cares/2018-03-24-142423_1360x768_scrot.png'
image_path_3='/home/pi/Desktop/FSSAI_Cares/2018-03-24-142423_1360x768_scrot.png'

def load_image_1():
	screen.fill((255,255,255))
	picture=pygame.image.load(image_path)
	screen.blit(picture,(0,0))
	pygame.display.update()

def load_image_2():
	screen.fill((255,255,255))
	picture=pygame.image.load(image_path)
	screen.blit(picture,(0,0))
	pygame.display.update()

def load_image_3():
	screen.fill((255,255,255))
	picture=pygame.image.load(image_path)
	screen.blit(picture,(0,0))
	pygame.display.update()


def exit_program():
	'''if play_story_1.process is not None and play_story_1.status() == 'playing':
		play_story_1.kill()
	if play_story_2.process is not None and play_story_2.status() == 'playing':
		play_story_2.kill()
	if play_story_3.process is not None and play_story_3.status() == 'playing':
		play_story_3.kill()'''
	if play_stories[0].process is not None and play_stories[0].status() == 'playing':
		play_stories[0].kill()
def shutdown():
	os.system("sudo shutdown -h now")
	#text-shutting down
	display_text("shutting down..")
	exit_program()
	
#print(GPIO.RPI_INFO)
GPIO.setmode(GPIO.BOARD)
mypin = 4
GPIO.setup(mypin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#load_image()
try:
    while(True):
        
        #load_image()
        # Video 0
        while GPIO.input(mypin):
            # waiting for low signal
            time.sleep(0.1)
            
        oldStoryIndex = 2
        storyIndex = 0

        print("Loading: " + str(storyIndex))
        play_stories[storyIndex].play()
        while play_stories[storyIndex].process is None:
            #wait for video to initialize
            time.sleep(0.1)
        while play_stories[storyIndex].status() != 'playing':
            #wait for video to start playing
            time.sleep(0.1)

        if play_stories[oldStoryIndex].process is not None and play_stories[oldStoryIndex].status() == 'playing':
            print("Stopping: " + str(oldStoryIndex))
            play_stories[oldStoryIndex].stop()

        #print("5 sec sleep")
        time.sleep(2)
        #os.system("killall omxplayer.bin")
        print("Pausing: " + str(storyIndex))
        play_stories[storyIndex].toggle()   #pause video

        while not GPIO.input(mypin):
            # waiting for high signal
            time.sleep(0.1)
 
        print("Playing: " + str(storyIndex))
        play_stories[storyIndex].toggle()   #play video


       # load_image()
        # Video 1
        while GPIO.input(mypin):
            # waiting for low signal
            time.sleep(0.1)
            
        oldStoryIndex = 0
        storyIndex = 1

        print("Loading: " + str(storyIndex))
        play_stories[storyIndex].play()
        while play_stories[storyIndex].process is None:
            #wait for video to initialize
            time.sleep(0.1)
        while play_stories[storyIndex].status() != 'playing':
            #wait for video to start playing
            time.sleep(0.1)

        if play_stories[oldStoryIndex].process is not None and play_stories[oldStoryIndex].status() == 'playing':
            print("Stopping: " + str(oldStoryIndex))
            play_stories[oldStoryIndex].stop()

        #print("5 sec sleep")
        time.sleep(2)
        #os.system("killall omxplayer.bin")
        print("Pausing: " + str(storyIndex))
        play_stories[storyIndex].toggle()   #pause video

        while not GPIO.input(mypin):
            # waiting for high signal
            time.sleep(0.1)
 
        print("Playing: " + str(storyIndex))
        play_stories[storyIndex].toggle()   #play video



       # load_image()
        # Video 2
        while GPIO.input(mypin):
            # waiting for low signal
            time.sleep(0.1)
            
        oldStoryIndex = 1
        storyIndex = 2

        print("Loading: " + str(storyIndex))
        play_stories[storyIndex].play()
        while play_stories[storyIndex].process is None:
            #wait for video to initialize
            time.sleep(0.1)
        while play_stories[storyIndex].status() != 'playing':
            #wait for video to start playing
            time.sleep(0.1)

        if play_stories[oldStoryIndex].process is not None and play_stories[oldStoryIndex].status() == 'playing':
            print("Stopping: " + str(oldStoryIndex))
            play_stories[oldStoryIndex].stop()

        #print("5 sec sleep")
        time.sleep(2)
        #os.system("killall omxplayer.bin")
        print("Pausing: " + str(storyIndex))
        play_stories[storyIndex].toggle()   #pause video

        while not GPIO.input(mypin):
            # waiting for high signal
            time.sleep(0.1)
 
        print("Playing: " + str(storyIndex))
        play_stories[storyIndex].toggle()   #play video
        
        
except KeyboardInterrupt:
    GPIO.cleanup()
    #exit_program()
    print('Exiting...')