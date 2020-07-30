# Assignment 29-07-2563 
#Sathaporn Phila 6201012630096
#----------------------------------------------------------------
import pygame
import pygame.camera
from pygame.locals import *
import sys
class picture :
    
    def __init__(self,M,N,width,height,id):
        self.x = M*width
        self.y = N*height
        self.width = width
        self.height = height
        self.id = id
    
    # create black rectangle with green frame
    def rect(self):   
        rectangle = (self.x,self.y,self.width,self.height)
        pygame.draw.rect(surface,(0,255,0),rectangle,1)      

def open_camera( frame_size=(640,480),mode='RGB'):
    pygame.camera.init()
    list_cameras = pygame.camera.list_cameras()
    if list_cameras:
        # use the first camera found
        camera = pygame.camera.Camera(list_cameras[0], frame_size, mode )
        return camera 
    return None

#create first time
def first_create(scr_w,scr_h,M,N):
    global system
    id = 0
    picture_width = scr_w//M
    picture_height = scr_h//N
    for j in range(N):
        for i in range(M):
            id += 1
            # draw a green frame (tile)
            name_id = "ID"+str(id)
            system.append(name_id)
            system[-1] = picture(i,j,picture_width,picture_height,id)
    for item in system :
        item.rect()

#find index of system list to create image
def get_locate_of_system_index(x,y):
    index_i = ((x//(scr_w//M))//1)
    index_j = ((y//(scr_h//N))//1)
    locate = ((M*index_j)+index_i)
    return locate


global scr_w,scr_h,M,N
scr_w, scr_h = 640, 480
M,N = 10,8

#store a rectangle
system = []

#a rectangle that using create image
system_active = []
pygame.init()

screen = pygame.display.set_mode((scr_w, scr_h))
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

#boolean value
img = None
is_running = True
initialization = True
close_camera = True

camera = open_camera()
if camera:
    camera.start()
else:
    print('Cannot open camera')
    sys.exit(-1)
while is_running:
    if close_camera == False :
        #try to capture            
        img = camera.get_image()
        if img is None:
            continue
        # get the image size
        img_rect = img.get_rect()
        img_w, img_h = img_rect.w, img_rect.h
        #create image
        for item in system_active :
            rectangle = (item.x,item.y,item.width,item.height)
            pygame.draw.rect(img,(0,255,0),rectangle,1)
            surface.blit( img , rectangle, rectangle )

    for e in pygame.event.get():

        #stop module
        if (e.type == pygame.QUIT) or ((e.type == KEYDOWN) and (e.key == K_ESCAPE)):
            is_running = False
            if img:
                print("image save")
                # save the current image into the output file
                pygame.image.save( screen, 'image.jpg' )

        if e.type == pygame.MOUSEBUTTONDOWN:

            #when click and all of screen are black
            if close_camera:
                close_camera = False
                mouse_position = pygame.mouse.get_pos()
                locate = get_locate_of_system_index(mouse_position[0],mouse_position[1])
                system_active.append(system[locate])
            
            #when it has an image
            else:
                mouse_position = pygame.mouse.get_pos()
                locate = get_locate_of_system_index(mouse_position[0],mouse_position[1])

                # when a rectangle you clicked is image
                if system[locate] in system_active :
                    pass

                # when a rectangle you clicked is black rectangle
                else :
                    system_active.append(system[locate])
    
    if initialization == True :
        initialization = False
        first_create(scr_w,scr_h,M,N)
    screen.blit( surface, (0,0) )
    pygame.display.update()

# close the camera
camera.stop()

print('Done....')
###################################################################
