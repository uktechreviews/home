#!/usr/bin/python3
import sys, pygame
from pygame.locals import *
import time
import subprocess
import os
from energenie import switch_on, switch_off
import io
import socket
import struct
from PIL import Image
import string


os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
pygame.init()

pygame.display.set_caption("Motion Camera")

def status():
  pygame.draw.rect(screen, black, (160,14,325,246),0)
  uptime = subprocess.check_output("uptime", shell=True )
  uptime = str(uptime)
  uptime = uptime[3:]
  uptime = uptime[:-4]
  font2=pygame.font.Font(None,18)
  ups = uptime.split("load")
  print (ups[0])
  label=font2.render(ups[0], 1, (white))
  screen.blit(label,(160,16))  

  hostname = subprocess.check_output("hostname -I", shell=True )
  hostname = str(hostname)
  hostname = hostname[2:]
  hostname = hostname[:-4]
  print (hostname)
  label2=font2.render(hostname, 1, (white))
  screen.blit(label2,(160,36)) 

  pi_temp = subprocess.check_output("/opt/vc/bin/vcgencmd measure_temp", shell=True )
  pi_temp = str(pi_temp)
  pi_temp = pi_temp[2:]
  pi_temp = pi_temp[:-5]
  print (pi_temp)
  label3=font2.render(pi_temp, 1, (white))
  screen.blit(label3,(160,56))

  ping_status = subprocess.getoutput("ping -c 1 10.0.1.13")
  if "error" in ping_status:
    error = "You can't get to the remote camera"
    label4=font2.render(error, 1, (red))
    screen.blit(label4,(160,76))
  else:
    text = "The camera is cuurently connected"
    label4=font2.render(text, 1, (white))
    screen.blit(label4,(160,76))

def shut_down():
  pygame.draw.rect(screen, red, (160,14,325,246),0)
  font5=pygame.font.Font(None,24)
  error = "MPC and Lights switched off"
  label4=font5.render(error, 1, (white))
  screen.blit(label4,(160,16))
  switch_off(1)
  error = "The system will shut down in 2 minutes"
  label4=font5.render(error, 1, (white))
  screen.blit(label4,(160,46))
  error = "Please unplug once the Pi is switched off"
  label4=font5.render(error, 1, (white))
  screen.blit(label4,(160,66))

#  subprocess.call("sudo shutdown -h +2 ", shell=True)
  



#define function for printing text in a specific place and with a specific colour and adding a border
def make_button(text, xpo, ypo, colour):
	font=pygame.font.Font(None,24)
	label=font.render(str(text), 1, (colour))
	screen.blit(label,(xpo,ypo))
	pygame.draw.rect(screen, cream, (xpo-5,ypo-5,110,35),1)

#define function that checks for mouse location
def on_click():
        click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])

##        if 550 <= click_pos[0] <= 600 and 155 <= click_pos[1] <=235:
##                button(0)

        if 15 <= click_pos[0] <= 125 and 15 <= click_pos[1] <=50:
                button(1)

        if 15 <= click_pos[0] <= 125 and 65 <= click_pos[1] <=100:
                button(2)

        if 15 <= click_pos[0] <= 125 and 115 <= click_pos[1] <=150:
                button(3)

        if 15 <= click_pos[0] <= 125 and 165 <= click_pos[1] <=200:
                button(4)

        if 15 <= click_pos[0] <= 125 and 215 <= click_pos[1] <=250:
                button(5)

        if 15 <= click_pos[0] <= 125 and 295 <= click_pos[1] <=355:
                button(13)

        if 655 <= click_pos[0] <= 765 and 15 <= click_pos[1] <=50:
                button(14)
                
        #now check to see if status was pressed
        if 15 <= click_pos[0] <= 125 and 265 <= click_pos[1] <=300:
                button(12)
                
        
def check_cam_IP():
  pygame.draw.rect(screen, black, (160,14,326,247),0)
  ping_status = subprocess.getoutput("ping -c 1 10.0.1.13")
  print (ping_status) #Take this out later
  if "error" in ping_status:
    error_cam=pygame.image.load("error.png")
    screen.blit(error_cam,(160,14))
    print ("You can't get to the remote camera")
    error = "Camera Network Error"
    font3=pygame.font.Font(None,30)
    label4=font3.render(error, 1, (blue))
    screen.blit(label4,(200,100))
    return
  else:
    camera_viewer()

def camera_viewer():
    print('I am happy that there is a camera connection')
    # Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0
    # means all interfaces)
    with socket.socket() as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', 8000))
        server_socket.listen(1)
        # Accept a single connection and make a file-like object out of it
        connection = server_socket.accept()[0].makefile('rb')
        try:
            while True:
                # Read the length of the image as a 32-bit unsigned int. If the
                # length is zero, quit the loop
                image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
                if not image_len:
                    break
                # Construct a stream to hold the image data and read the image
                # data from the connection
                image_stream = io.BytesIO()
                image_stream.write(connection.read(image_len))
                # Rewind the stream, open it as an image with PIL and do some
                # processing on it
                
                image_stream.seek(0)
##                        image = Image.open(image_stream)
                cctv=pygame.image.load(image_stream)
                screen.blit(cctv,(160,14))
                pygame.display.flip()
                font2=pygame.font.Font(None,14)
                label=font2.render("Live", 1, (red))
                screen.blit(label,(450,567))


        finally:
                pygame.draw.rect(screen, black, (160,14,600,350),0)
                pygame.display.flip()

                print ("End of camera work")
                connection.close()



#define action on pressing buttons
def button(number):

    if number == 13:
            shut_down()

    if number == 12:
            status()
            
    if number == 1:
            switch_on(2)
            
    if number == 2:
            switch_off(2)

    if number == 3:
            switch_on(1)

    if number == 4:
            switch_off(1)

    if number == 5:
            check_cam_IP()


#set size of the screen
size = width, height = 790, 390

#define colours
blue = 26, 0, 255
cream = 254, 255, 250
black = 0, 0, 0
white = 255, 255, 255
red = 255,0,0
green = 0,255,0
yellow = 255, 255, 224

screen = pygame.display.set_mode(size)
#pygame.display.set_mode((790,390),pygame.FULLSCREEN)

#set up the fixed items on the menu
screen.fill(blue) #change the colours if needed
pygame.draw.rect(screen, white, (0,0,790,390),1)
pygame.draw.rect(screen, black, (160,14,600,350),0)
font2=pygame.font.Font(None,14)
label=font2.render("CCTV Feed", 1, (white))
screen.blit(label,(175,420))

                 

#Add buttons and labels
make_button("Remote on", 20, 20, white)
make_button("Remote off", 20, 70, white)
make_button("Lights on", 20, 120, white)
make_button("Lights off", 20, 170, white)
make_button("Stream", 20, 220, white)
make_button("Status",20, 270, white)
make_button("Shutdown",20, 320, red)

#While loop to manage touch screen inputs
while 1:

        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
                        on_click()

        #ensure there is always a safe way to end the program if the touch screen fails

                if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                                switch_off(1)
                                switch_off(2)
                                sys.exit()
        pygame.display.update()
refresh_menu_screen()  #refresh the menu interface


main()
