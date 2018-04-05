from video_player import *
import RPi.GPIO as GPIO
import time
import pygame
import sys

pygame.init()
pygame.mouse.set_visible(False)
infoObject = pygame.display.Info()
screen=pygame.display.set_mode((infoObject.current_w, infoObject.current_h),pygame.NOFRAME)
screen=pygame.display.set_mode((1280,1024),pygame.NOFRAME)

if len(sys.argv) > 1:
    arg = sys.argv[1]
else:
    arg = '0'

BASE_DIR = '/home/pi/Desktop/FSSAI_Cares/'

FILENAME_VIDEO_1 =  'FSSAI_Care_Videos/Comic_1/Scene_' + arg + '.mp4'
FILENAME_VIDEO_2 =  'FSSAI_Care_Videos/Comic_2/Scene_' + arg + '.mp4'
FILENAME_VIDEO_3 =  'FSSAI_Care_Videos/Comic_3/Scene_' + arg + '.mp4'

FILENAME_IMAGE_1 =  'FSSAI_Care_Images/Comic_1/Scene_' + arg + '.png'
FILENAME_IMAGE_2 =  'FSSAI_Care_Images/Comic_2/Scene_' + arg + '.png'
FILENAME_IMAGE_3 =  'FSSAI_Care_Images/Comic_3/Scene_' + arg + '.png'

play_path_video_story_1 = ''.join([BASE_DIR, FILENAME_VIDEO_1])
play_path_video_story_2 = ''.join([BASE_DIR, FILENAME_VIDEO_2])
play_path_video_story_3 = ''.join([BASE_DIR, FILENAME_VIDEO_3])

play_path_image_story_1 = ''.join([BASE_DIR, FILENAME_IMAGE_1])
play_path_image_story_2 = ''.join([BASE_DIR, FILENAME_IMAGE_2])
play_path_image_story_3 = ''.join([BASE_DIR, FILENAME_IMAGE_3])

videos = [Player(play_path_video_story_1), Player(play_path_video_story_2), Player(play_path_video_story_3)]
images = [pygame.image.load(play_path_image_story_1).convert(), pygame.image.load(play_path_image_story_2).convert(), pygame.image.load(play_path_image_story_3).convert()]

oldStoryIndex = 1
storyIndex = 2

mypin = 11
resetPin = 13
shutdownPin = 15

hasShutdown = False

GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
GPIO.setup(mypin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(resetPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(shutdownPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def exit_program():
    for video in videos:
        if video.process is not None and video.status() == 'playing':
            video.kill()
    
    pygame.quit()
    GPIO.cleanup()

def shutdown():
    global hasShutdown
    if not hasShutdown:
        os.system("sudo shutdown -h now")
        #text-shutting down
        print("shutting down..")
        exit_program()
        hasShutdown = True

try:
    while(True):
        while GPIO.input(mypin):
            # waiting for low signal
            time.sleep(0.1)
            if GPIO.input(shutdownPin):
                print("shutdown!")
                shutdown()

        oldStoryIndex = storyIndex
        storyIndex += 1
        if storyIndex > 2:
            storyIndex = 0

        if GPIO.input(resetPin):
            storyIndex = 0

        print("Loading image: " + str(storyIndex))
        screen.fill((0,0,0))
        screen.blit(images[storyIndex], (0,0))
        pygame.display.flip()
        
        time.sleep(0.1)
        
        if videos[oldStoryIndex].process is not None and videos[oldStoryIndex].status() == 'playing':
            print("Stopping: " + str(oldStoryIndex))
            videos[oldStoryIndex].stop()

        while not GPIO.input(mypin):
            # waiting for high signal
            time.sleep(0.1)
            if GPIO.input(shutdownPin):
                print("shutdown!")
                shutdown()
 
        print("Playing: " + str(storyIndex))
        videos[storyIndex].play()   #play video
        
except KeyboardInterrupt:
    GPIO.cleanup()
    pygame.quit()
    #exit_program()
    print('Exiting...')