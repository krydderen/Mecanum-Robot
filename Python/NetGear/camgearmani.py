# import required libraries
from vidgear.gears import CamGear
import cv2

# Open any source of your choice, like Webcam first index(i.e. 0) and change its colorspace to `HSV`
stream = CamGear(source=0, colorspace = 'COLOR_BGR2HSV', logging=True).start()

# loop over
while True:

    # read HSV frames
    frame = stream.read()

    # check for frame if Nonetype
    if frame is None:
        break


    # {do something with the HSV frame here}


    # Show output window
    cv2.imshow("Output Frame", frame)

    # check for key if pressed
    key = cv2.waitKey(1) & 0xFF

    # check if 'w' key is pressed
    if key == ord("w"):
        #directly change colorspace at any instant
        stream.color_space = cv2.COLOR_BGR2GRAY #Now colorspace is GRAY

    # check for 'e' key is pressed
    if key == ord("e"):
        stream.color_space = cv2.COLOR_BGR2LAB  #Now colorspace is CieLAB

    # check for 'r' key is pressed
    if key == ord("r"):
         stream.color_space = None #Now colorspace is default(ie BGR)

    # check for 'q' key is pressed
    if key == ord("q"):
      break

# close output window
cv2.destroyAllWindows()

# safely close video stream
stream.stop()