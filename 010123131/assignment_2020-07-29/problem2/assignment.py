# Assignment 31-07-63
# Sathaporn Phila 6201012630096
#----------------------------------------------------------------------------
import pygame
from pygame.locals import *
import pygame.camera
import sys

class picture :
    def __init__(self,M,N,width,height,id):
        self.x = M*width
        self.y = N*height
        self.width = width
        self.height = height
        self.id = id
    
    def rect(self):
        rectangle = (self.x,self.y,self.width,self.height)
        pygame.draw.rect(surface,(0,255,0),rectangle,1)
        surface.blit(surface,rectangle,rectangle)
    def rect_with_img(self,img):
        rectangle = (self.x,self.y,self.width,self.height)
        pygame.draw.rect(img,(0,255,0),rectangle,1)
        surface.blit(img,rectangle,rectangle)
    def move(self,x,y,img):
        rectangle = (self.x,self.y,self.width,self.height)
        self.x = x
        self.y = y
        print(x,y,rectangle,self.id,img.get_rect())
        pygame.draw.rect(img,(0,255,0),rectangle,1)
        surface.blit(img,(x,y),rectangle)

#create first time
def first_create(scr_w,scr_h,M,N):
    global system
    system = []
    id = 0
    picture_width = scr_w//M
    picture_height = scr_h//N
    for j in range(N):
        for i in range(M):
            # draw a green frame (tile)
            name_id = "ID"+str(id)
            system.append(name_id)
            system[-1] = picture(i,j,picture_width,picture_height,id)
            id += 1
    for item in system :
        item.rect()
        

def open_camera( frame_size=(640,480),mode='RGB'):
    pygame.camera.init()
    list_cameras = pygame.camera.list_cameras()
    print( 'Mumber of cameras found: ', len(list_cameras) )
    if list_cameras:
        # use the first camera found
        camera = pygame.camera.Camera(list_cameras[0], frame_size, mode )
        return camera 
    return None 

scr_w, scr_h = 640, 480
pygame.init()
global system,img,system_store
system = []
system_store = []
camera = open_camera()
if camera:
    camera.start()
else:
    print('Cannot open camera')
    sys.exit(-1)

screen = pygame.display.set_mode((scr_w, scr_h))
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

M,N = 10,8

is_running = True
initialization = True
drag = False
target_start_drag = False
img = None
capture = True

#find idex
def get_locate_of_system_index(x,y):
    index_i = ((x//(scr_w//M))//1)
    index_j = ((y//(scr_h//N))//1)
    locate = ((M*index_j)+index_i)
    return locate

def find_item(x,y):
    global system_store
    locate = get_locate_of_system_index(x,y)
    item = system[locate]
    print(item)
    if len(system_store) == 0 :
        system_store.append(item)
    else:
        #when index you choose is repeated,save image and load again
        if item in system_store :
            system_store = []
            print('1')
            pygame.image.save(screen,'img2.jpg')
            print('img')
            img = pygame.image.load(r'C:\Users\User\rsp\img2.jpg')
            first_create(scr_w,scr_h,M,N)
            for item in system :
                item.rect_with_img(img)
            item = system[locate]
            system_store.append(item)
        else:
            system_store.append(item)
    print(system_store)
    x_locate = item.x
    y_locate = item.y
    return (item,x_locate,y_locate,locate)


while is_running :

    for e in pygame.event.get():
        if (e.type == pygame.QUIT) or ((e.type == KEYDOWN) and (e.key == K_ESCAPE)):
            if img :
                pygame.image.save(screen,"picture_assignment_4.jpg")
                is_running = False
        elif e.type == pygame.MOUSEBUTTONDOWN :
            if pygame.MOUSEBUTTONDOWN  :
                drag = True
        elif e.type == pygame.MOUSEBUTTONUP:
            if pygame.MOUSEBUTTONUP :
                position = pygame.mouse.get_pos()
                x = position[0]
                y = position[1]
                item_stop = find_item(x,y)
                index_of_item_start,index_of_item_stop = item_start[3],item_stop[3]
                item_start[0].move(item_stop[1],item_stop[2],img) #switch
                item_stop[0].move(item_start[1],item_start[2],img) #switch
                system[index_of_item_start] = item_stop[0]
                system[index_of_item_start].id = index_of_item_start
                system[index_of_item_stop] = item_start[0]
                system[index_of_item_stop].id = index_of_item_stop       
                drag = False
                target_start_drag = False
                
        elif e.type == pygame.MOUSEMOTION:
            if drag:
                position = pygame.mouse.get_pos()
                x = position[0]
                y = position[1]
                if  target_start_drag == False:
                    item_start = find_item(x,y)
                    target_start_drag = True
                
                
                    
    if initialization :
        initialization = False
        first_create(scr_w,scr_h,M,N)
        time = 0 
        while capture == True and time < 300 :
            img = camera.get_image()
            if img == None :
                continue
            for item in system :
                rectangle = (item.x,item.y,item.width,item.height)
                pygame.draw.rect(img,(0,255,0),rectangle,1)
                surface.blit(img,rectangle,rectangle)
                
            time += 1
            print(time)
            screen.blit( surface, (0,0) )
            pygame.display.update()
        pygame.image.save(screen,'img2.jpg')
        print("save")
        img = pygame.image.load(r'C:\Users\User\rsp\img2.jpg')
        first_create(scr_w,scr_h,M,N)
        for item in system :
            item.rect_with_img(img)

    screen.blit( surface, (0,0) )
    pygame.display.update()
camera.stop()

print('Done....')
