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


os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
pygame.init()

#define function for printing text in a specific place and with a specific colour and adding a border
def make_button(text, xpo, ypo, colour):
	font=pygame.font.Font(None,24)
	label=font.render(str(text), 1, (colour))
	screen.blit(label,(xpo,ypo))
	pygame.draw.rect(screen, cream, (xpo-5,ypo-5,110,35),1)

#define function that checks for mouse location
def on_click():
        click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])

        if 500 <= click_pos[0] <= 600 and 130 <= click_pos[1] <=230:
                button(0)

        if 15 <= click_pos[0] <= 125 and 15 <= click_pos[1] <=50:
                button(1)

        if 15 <= click_pos[0] <= 125 and 65 <= click_pos[1] <=100:
                button(2)

        if 15 <= click_pos[0] <= 125 and 115 <= click_pos[1] <=150:
                button(3)

        if 15 <= click_pos[0] <= 125 and 165 <= click_pos[1] <=200:
                button(4)

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
                screen.blit(cctv,(170,0))
                pygame.display.flip()
##                        print('Image is %dx%d' % image.size)
##                        image.verify()
##                        print('Image is verified')
        finally:
                print ("End of camera work")
                connection.close()



#define action on pressing buttons
def button(number):

        if number == 0:    #specific script when exiting
                screen.fill(black)
                font=pygame.font.Font(None,36)
                label=font.render("Good Bye!", 1, (white))
                screen.blit(label,(105,120))
                pygame.display.flip()
                time.sleep(5)
                sys.exit()

        if number == 1:
                camera_viewer()


        if number == 2:
                switch_off(2)

        if number == 3:
                switch_on(1)

        if number == 4:
                switch_off(1)

#set size of the screen
size = width, height = 640, 240

#define colours
blue = 26, 0, 255
cream = 254, 255, 250
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)

#set up the fixed items on the menu
screen.fill(blue) #change the colours if needed
logo=pygame.image.load("logo.tiff")
exit=pygame.image.load("exit.tiff")
screen.blit(logo,(510,5))
screen.blit(exit,(500,130))
pygame.draw.rect(screen, white, (0,0,640,240),1)

#Add buttons and labels
make_button("Lamp on", 20, 20, white)
make_button("Lamp off", 20, 70, white)
make_button("XBox360 on", 20, 120, white)
make_button("XBox 360 off", 20, 170, white)

#While loop to manage touch screen inputs
while 1:
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
                        on_click()

        #ensure there is always a safe way to end the program if the touch screen fails

                if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                                sys.exit()
        pygame.display.update()
refresh_menu_screen()  #refresh the menu interface


main()
