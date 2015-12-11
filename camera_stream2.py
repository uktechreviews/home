import io
import socket
import struct
import time
import picamera

while True:

    with picamera.PiCamera() as camera:
        camera.resolution = (150, 115)
        # Start a preview and let the camera warm up for 2 seconds
    ##    camera.start_preview()
        time.sleep(2)

        while True:
            with socket.socket() as client_socket:
                try:
                    # Connect a client socket to my_server:8000 (change my_serv$
                    # hostname of your server)
                    client_socket.connect(('10.0.1.3', 8000))
                except (OSError, IOError) as e:
                    print('Failed to connect, sleeping for a while')
                    time.sleep(1)
                else:
                    print('Connected, streaming')
                    # Make a file-like object out of the connection
                    connection = client_socket.makefile('wb')
                    try:
                        # Note the start time and construct a stream to hold im$
                        # data temporarily (we could write it directly to
                        # connection but in this case we want to find out the s$
                        # of each capture first to keep our protocol simple)
                        start = time.time()
                        stream = io.BytesIO()
                        for foo in camera.capture_continuous(stream, 'jpeg'):
                            # Write the length of the capture to the stream and$
                            # ensure it actually gets sent
                            connection.write(struct.pack('<L', stream.tell()))
                            connection.flush()
                            # Rewind the stream and send the image data over th$
                            stream.seek(0)
                            connection.write(stream.read())
                            # If we've been capturing for more than 30 seconds,$
                            if time.time() - start > 5:
                                break
                            # Reset the stream for the next capture
                            stream.seek(0)
                            stream.truncate()
                        # Write a length of zero to the stream to signal we're $
                        connection.write(struct.pack('<L', 0))
                        connection.close()
                        client_socket.shutdown(socket.SHUT_RDWR)

                    finally:
                        break


