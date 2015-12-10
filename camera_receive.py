import io
import socket
import struct
from PIL import Image

while True:
    print('Press Enter to stream')
    input()
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
                image = Image.open(image_stream)
                cctv=pygame.image.load(image_stream)
                screen.blit(cctv,(170,0))
                pygame.display(flip)
                print('Image is %dx%d' % image.size)
                image.verify()
                print('Image is verified')
        finally:
            connection.close()

