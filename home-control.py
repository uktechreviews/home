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

def show_playlist():
        play_list = subprocess.check_output("mpc playlist", shell=True )
        play_list = str(play_list)
        play_list = play_list[2:]
        play_list = play_list[:-1]
        plays = play_list.split("\\n")
        font2=pygame.font.Font(None,18)
        offset = 0
        for play in plays:
                print (play)
                play = play[:45]
                label=font2.render(play, 1, (white))
                screen.blit(label,(160,16+offset))
                offset +=20


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
                
        #now check to see if play was pressed
        if 510 <= click_pos[0] <= 555 and 16 <= click_pos[1] <=65:
                print ("You pressed button play")
                button(6)

        #now check to see if stop  was pressed
        if 565 <= click_pos[0] <= 605 and 16 <= click_pos[1] <=65:
                print ("You pressed button stop")
                button(7)

         #now check to see if volume down was pressed
        if 510 <= click_pos[0] <= 555 and 160 <= click_pos[1] <=200:
                print ("You pressed volume down")
                button(8)

         #now check to see if volume up was pressed
        if 565 <= click_pos[0] <= 605 and 160 <= click_pos[1] <=200:
                print ("You pressed volume up")
                button(9)

        #now check to see if previous  was pressed
        if 510 <= click_pos[0] <= 555 and 75 <= click_pos[1] <=105:
                print ("You pressed button previous")
                button(10)

         #now check to see if next  was pressed
        if 565 <= click_pos[0] <= 605 and 75 <= click_pos[1] <=105:
                print ("You pressed button next")
                button(11)

        #now check to see if refresh  was pressed
        if 581 <= click_pos[0] <= 625 and 294 <= click_pos[1] <=315:
                print ("You pressed button refresh")
                show_playlist()
                 
def camera_viewer():
    print('Press Enter to stream')
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
                screen.blit(label,(250,267))


        finally:
                pygame.draw.rect(screen, black, (160,14,326,247),0)
                pygame.display.flip()
                pygame.draw.rect(screen, blue, (250,267,75,10),0)

                print ("End of camera work")
                connection.close()



#define action on pressing buttons
def button(number):

    if number == 1:
            switch_on(2)
            
    if number == 2:
            switch_off(2)

    if number == 3:
            switch_on(1)

    if number == 4:
            switch_off(1)

    if number == 5:
            camera_viewer()

    if number == 6:	
            subprocess.call("mpc play ", shell=True)

    if number == 7:
            subprocess.call("mpc stop ", shell=True)

    if number == 8:
            subprocess.call("mpc volume -2 ", shell=True)
  
    if number == 9:
            subprocess.call("mpc volume +2 ", shell=True)

    if number == 10:
            subprocess.call("mpc prev ", shell=True)

    if number == 11:
            subprocess.call("mpc next ", shell=True)


    pygame.draw.rect(screen, yellow, (163,290, 420, 40),0)
    station_font=pygame.font.Font(None,20)
    title_font=pygame.font.Font(None,34)
    station = subprocess.check_output("mpc current", shell=True )
    station=str(station)
    print (station)
    lines=station.split(":")
    print (lines)
    length = len(lines) 
    if length==1:
            line1 = lines[0]
            line2 = "No additional info: "
    else:
            line1 = lines[0]
            line2 = lines[1]
            
    line1 = line1.replace("b'", "")
    line1 = line1[:45]
    line2 = line2[:45]
    line2 = line2[:-3]
    print ("line1")
    print (line1)
    print ("line2")
    print (line2)
    #trap no station data
    if line1 =="'":
            line1 = "No Station information available"
            line2 = "Press PLAY or REFRESH"
            station_status = "stopped"
            status_font = red
    else:
            station_status = "playing"
            status_font = green
    station_name=station_font.render(line1, 1, (red))
    additional_data=station_font.render(line2, 1, (blue))
    station_label=title_font.render(station_status, 1, (status_font))
    screen.blit(station_label,(166,290))
    screen.blit(station_name,(270,295))
    screen.blit(additional_data,(270,315))
    pygame.draw.rect(screen, cream, (504,225, 120, 30),0)
    
##    check to see if the Radio is connected to the internet
    font=pygame.font.Font(None,22)
    IP = subprocess.check_output("hostname -I", shell=True )
    IP = str(IP)
    print (IP)
    if "10" in IP:
            network_status = "online"
            status_font = green

    else:
            network_status = "offline"
            status_font = red
    network_status_label = font.render(network_status, 1, (status_font))
    screen.blit(network_status_label, (505,230))
    volume = subprocess.check_output("mpc volume", shell=True )
    volume = volume[8:]
    volume = volume[:-1]
    if volume == "00%":
            volume = "max"
    volume_tag=font.render(volume, 1, (black))
    screen.blit(volume_tag,(560,230))
    pygame.display.flip()


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

#set up the fixed items on the menu
screen.fill(blue) #change the colours if needed
pygame.draw.rect(screen, white, (0,0,790,390),1)
pygame.draw.rect(screen, black, (160,14,325,246),0)
font2=pygame.font.Font(None,14)
label=font2.render("CCTV Feed", 1, (white))
screen.blit(label,(175,267))
#Add radioplayer control
play=pygame.image.load("play.tiff")
pause=pygame.image.load("pause.tiff")
refresh=pygame.image.load("refresh.tiff")
previous=pygame.image.load("previous.tiff")
next=pygame.image.load("next.tiff")
vol_down=pygame.image.load("volume_down.tiff")
vol_up=pygame.image.load("volume_up.tiff")
pygame.draw.rect(screen, cream, (504,14,120, 200),0)
pygame.draw.rect(screen, cream, (504,225, 120, 30),0)
pygame.draw.rect(screen, blue, (504,145, 120, 10),0)
pygame.draw.rect(screen, yellow, (163,290, 420, 40),0)
pygame.draw.rect(screen, white, (585,290,40,40),0)
screen.blit(play,(510,16))
screen.blit(previous,(510,75))
screen.blit(next,(565,75))
screen.blit(vol_down,(510,160))
screen.blit(vol_up,(565,160))
screen.blit(pause,(565,16))
screen.blit(refresh,(581,294))
                 

#Add buttons and labels
make_button("Mac on", 20, 20, white)
make_button("Mac off", 20, 70, white)
make_button("Lights on", 20, 120, white)
make_button("Lights off", 20, 170, white)
make_button("Front door", 20, 220, white) 

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
