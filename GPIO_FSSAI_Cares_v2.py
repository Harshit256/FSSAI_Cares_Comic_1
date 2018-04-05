from video_player import *
import RPi.GPIO as GPIO
import time
import pygame

pygame.init()
pygame.mouse.set_visible(False)
infoObject = pygame.display.Info()
screen=pygame.display.set_mode((infoObject.current_w, infoObject.current_h),pygame.NOFRAME)
screen=pygame.display.set_mode((1280,1024),pygame.NOFRAME)
BASE_DIR = '/home/pi/Desktop/FSSAI_Cares/'

FILENAME_VIDEO_1 =  'FSSAI_Care_Videos/Comic_1/Scene_0.mp4'
FILENAME_VIDEO_2 =  'FSSAI_Care_Videos/Comic_2/Scene_0.mp4'
FILENAME_VIDEO_3 =  'FSSAI_Care_Videos/Comic_3/Scene_0.mp4'

FILENAME_IMAGE_1 =  'FSSAI_Care_Images/Comic_1/Scene_0.png'
FILENAME_IMAGE_2 =  'FSSAI_Care_Images/Comic_2/Scene_0.png'
FILENAME_IMAGE_3 =  'FSSAI_Care_Images/Comic_3/Scene_0.png'

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

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
mypin = 3
GPIO.setup(mypin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

try:
    while(True):                    
        while GPIO.input(mypin):
            # waiting for low signal
            time.sleep(0.1)
            
        oldStoryIndex = storyIndex
        storyIndex += 1
        if storyIndex > 2:
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
 
        print("Playing: " + str(storyIndex))
        videos[storyIndex].play()   #play video
        
except KeyboardInterrupt:
    GPIO.cleanup()
    #exit_program()
    print('Exiting...')