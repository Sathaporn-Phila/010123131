####################################################################
# Author: RSP
# Dev. by Sathaporn Phila 6201012630096
# File: python_threading_demo-8.py
# Date: 2020-07-22
#####################################################################

import threading
import time
import cmath
import pygame
from random import randint, randrange, random

print( 'File:', __file__ )
# global variable
allow_threads_running = True 
def mandelbrot(c,max_iters=100):
    i = 0
    z = complex(0,0)
    while abs(z) <= 2 and i < max_iters:
        z = z*z + c
        i += 1 
    return i
def thread_func(id,N,lock,sem):
    global allow_threads_running
    while allow_threads_running:
        # try to acquire binary semaphore associated with the thread
        if not sem.acquire(timeout=0.1):
            # cannot acquire the semaphore after timeout, try again
            continue
        with lock:
            #divide N areas in x-axis
            scale = 0.006
            offset = complex(-0.55,0.0)
            scaling = ((scr_h + (scr_h%N))//N)
            for x in range(scr_w):
                for y in range(scaling):
                    y = (((id-1)*scaling)+y)
                    re = scale*(x-w2) + offset.real
                    im = scale*(y-h2) + offset.imag
                    c = complex( re, im )
                    color = mandelbrot(c, 63)
                    r = (color << 6) & 0xc0
                    g = (color << 4) & 0xc0
                    b = (color << 2) & 0xc0
                    surface.set_at( (x, y), (255-r,255-g,255-b) )

# initialize pygame
pygame.init()

# create a screen of width=600 and height=400
global scr_w,scr_h
scr_w = 500
scr_h = 500
screen = pygame.display.set_mode( (scr_w, scr_h) )

# set window caption
pygame.display.set_caption('Fractal Image: Mandelbrot') 

# create a clock
clock = pygame.time.Clock()

# create a surface for drawing
surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

first_create = True 

running = True
global w2,h2 # half width, half screen
w2 = scr_w//2
h2 = scr_h//2
#---------------------Thread initialization------------------------#
# set the number of threads to be created (e.g. N=13)
N = 13

# create a thread lock 
lock = threading.Lock()
# create a list of binary semaphores to be used for threads
list_sempahores = [ threading.Semaphore(0) for i in range(N) ]
# a list used to keep the threads
list_threads = []

# create a number of threads (e.g, N=13)
for i in range(N):
    id = (i+1)
    sem = list_sempahores[i]
    t = threading.Thread( target=thread_func, args=(id,N,lock,sem) )
    t.setName( 'Thread-%d' % id )
    list_threads.append( t )


#-------------------------------------------------------------
while running:

    if first_create:
        first_create = False
        # start each of the threads in the list
        for t in list_threads:
            t.start()
        #print thread
        for t in threading.enumerate():
            if t.isAlive() :
                print( '{} is active.'.format( t.getName( ) ) )
        for sem in list_sempahores: 
            sem.release()
        allow_threads_running = False 
        # force the main thread to wait until all threads are finished.
        for t in list_threads:
            t.join() 
    # draw the surface on the screen
    screen.blit( surface, (0,0) )
    # update the display
    pygame.display.update()

    clock.tick(1.0) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
print( 'PyGame done...')
################################################################
