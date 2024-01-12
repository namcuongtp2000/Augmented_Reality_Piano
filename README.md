# Augmented_Reality_Piano
Playing piano by computer vision, OpenCV and Mediapipe Hands

# Installation
pip install -r requirements.txt

# How it works
There are 3 dotted lines created by circles as interacting points: 
The lowest line (**A**) can be controled by 3 fingertips: 8.INDEX_FINGER_TIP , 12.MIDDLE_FINGE_TIP, 16.RING_FINGER_TIP from mediapipe for both hands.
The middle line (**B**) can only be controled by 20.PINKY_FINGER_TIP for both hands.
The highest line (**C**) can only be controled by 4.THUMB_FINGER_TIP for both hands.

Each note will be notated as its line prefix A,B or C and its number 1 to 61 from the right of screen to the left.For example, the most right note in lowest line will be notated as A1.
![image](https://github.com/namcuongtp2000/Augmented_Reality_Piano/assets/92356571/b3f0ebfa-9ee8-4c74-856b-fc48265a1d62)

The **RED** circles will play role as black keys of piano 61 keys while the **GREEN** circles represent for white keys.

You should run this app while your camera in bright light environment to make mediapipe hands easy to detect your fingertips.
# Future updates
- Increase the sensity and accuracy from touching interacting circles.
- Create a game to check the correct of the notes or chords in limitted time.
