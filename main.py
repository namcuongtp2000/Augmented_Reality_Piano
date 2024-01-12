import cv2
import mediapipe as mp
import pygame
import os
import math
import time
import subprocess
# Initialize Pygame
pygame.init()

# Set up Pygame sound
pygame.mixer.init()

# Specify the path to the sound files directory
sound_files_directory = 'sound_files'

# Get the list of sound files in the directory
sound_files = [os.path.join(sound_files_directory, file) for file in sorted(os.listdir(sound_files_directory)) if file.endswith('.wav')]
sounds = [pygame.mixer.Sound(file) for file in sound_files]

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Set the desired resolution
desired_width = 1280  # Set your desired width
desired_height = 720  # Set your desired height

# OpenCV Webcam Configuration
cap = cv2.VideoCapture(0)
cap.set(3, desired_width)  # Set width
cap.set(4, desired_height)  # Set height

# First circle line parameters
num_keys1 = 61
start_x1, end_x1, height1 = 28, 1268, desired_height / 2 + 310
circle_radius1 = 3
circle_positions1 = [(i * (end_x1 - start_x1) / num_keys1 + start_x1, height1) for i in reversed(range(num_keys1))]

# Second circle line parameters
num_keys2 = 61
start_x2, end_x2, height2 = 28, 1268, desired_height / 2 + 270
circle_radius2 = 3
circle_positions2 = [(i * (end_x2 - start_x2) / num_keys2 + start_x2, height2) for i in reversed(range(num_keys2))]

# Third circle line parameters
num_keys3 = 61
start_x3, end_x3, height3 = 28, 1268, desired_height / 2 + 230
circle_radius3 = 3
circle_positions3 = [(i * (end_x3 - start_x3) / num_keys3 + start_x3, height3) for i in reversed(range(num_keys3))]

# Define fingertip indices for each hand
left_hand_fingertips = {
    "A": [8, 12, 16],
    "B": [20],
    "C": [4]
}
right_hand_fingertips = {
    "A": [8, 12, 16],
    "B": [20],
    "C": [4]
}

# Dictionary to store circle positions and radii
circle_info = {
    "A": {"positions": circle_positions1, "radius": circle_radius1},
    "B": {"positions": circle_positions2, "radius": circle_radius2},
    "C": {"positions": circle_positions3, "radius": circle_radius3}
}

# Dictionary to store active sounds
active_sounds = {
    "A": [None] * num_keys1,
    "B": [None] * num_keys2,
    "C": [None] * num_keys3
}

# Dictionary to store the activation time of each note
activation_times = {
    "A": [0] * num_keys1,
    "B": [0] * num_keys2,
    "C": [0] * num_keys3
}

# Variables to track notes played during the last 1000 ms
last_1000ms_notes = {"A": [], "B": [], "C": []}
start_time_1000ms = time.time()

# Positions to be colored in red for each line
red_positions = {
    "A": [2, 4, 7, 9, 11, 14, 16, 19, 21, 23, 26, 28, 31, 33, 35, 38, 40, 43, 45, 47, 50, 52, 55, 57, 59],
    "B": [2, 4, 7, 9, 11, 14, 16, 19, 21, 23, 26, 28, 31, 33, 35, 38, 40, 43, 45, 47, 50, 52, 55, 57, 59],
    "C": [2, 4, 7, 9, 11, 14, 16, 19, 21, 23, 26, 28, 31, 33, 35, 38, 40, 43, 45, 47, 50, 52, 55, 57, 59]
}

while True:
    current_time = time.time()

    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(frame_rgb)

    # Draw circle lines
    for line, info in circle_info.items():
        for pos_index, pos in enumerate(info["positions"]):
            x, y = int(round(pos[0])), int(round(pos[1]))

            # Check if the position should be colored in red
            if pos_index + 1 in red_positions[line]:
                color = (0, 0, 255)  # Red color
            else:
                color = (0, 255, 0)  # Green color

            cv2.circle(frame, (x, y), info["radius"], color, 1)

    # Set the position and dimensions of the grid
    grid_x, grid_y, grid_width, grid_height = 20, 500, 1220, 200

    # Calculate the number of keys per line
    keys_per_line = num_keys1 - 1

    # Calculate the width of each small rectangle
    small_rect_width = grid_width / keys_per_line

    # Draw the grid
    for i in range(keys_per_line + 1):
        rect_x = int(grid_x + i * small_rect_width)
        rect_y = int(grid_y)
        rect_width = int(small_rect_width)
        rect_height = int(grid_height)

        # Draw the rectangle
        cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (255, 255, 255), 1)

        # Draw the circles on the rectangle
        for line, circle_positions in zip(["A", "B", "C"], [circle_positions1, circle_positions2, circle_positions3]):
            for pos in circle_positions:
                circle_x = int(pos[0])
                circle_y = int(pos[1])

                # Check if the circle is within the current small rectangle
                if rect_x <= circle_x <= rect_x + rect_width and rect_y <= circle_y <= rect_y + rect_height:
                    # Record the activated note or chord
                    note_prefix = f"{line}{pos_index + 1}"
                    

    # Check hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for line, fingertips in left_hand_fingertips.items():
                for i in fingertips:
                    # Get landmark position
                    landmark = hand_landmarks.landmark[i]
                    x, y = int(landmark.x * desired_width), int(landmark.y * desired_height)
                
                    # Check if the fingertip interacts with the circles and active sound files
                    for pos_index, pos in enumerate(circle_info[line]["positions"]):
                        dist = math.sqrt((x - pos[0]) ** 2 + (y - pos[1]) ** 2)

                        # Play sound and mark as active if the fingertip is within the circle
                        if dist < circle_info[line]["radius"]:
                            if active_sounds[line][pos_index] is None:
                                active_sounds[line][pos_index] = pygame.mixer.Sound(sound_files[pos_index])
                                active_sounds[line][pos_index].play()

                            # Record the activated note or chord
                            note_prefix = f"{line}{pos_index + 1}"
                            last_1000ms_notes[line].append(note_prefix)
                            last_1000ms_notes[line] = list(set(last_1000ms_notes[line]))[:10]

                            # Set the activation time when the note is activated
                            activation_times[line][pos_index] = current_time
                            
                            # Display text near the activated note with modified note names
                            cv2.putText(frame, note_prefix, (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                        
                        else:
                            # If the landmark is not within the circle, mark the sound as inactive
                            active_sounds[line][pos_index] = None

                    # Draw fingertip circles
                    cv2.circle(frame, (x, y), 6, (255, 0, 0), -1)

    # Check if 1000 ms have elapsed
    if current_time - start_time_1000ms >= 1.0:
        start_time_1000ms = current_time

        # Print the notes played during the last 1000 ms
        for line, notes in last_1000ms_notes.items():
            if len(notes) == 1:
                print(notes[0])
            elif len(notes) > 1:
                print(f"[{' '.join(notes)}]")

        # Clear the notes played during the last 1000 ms
        last_1000ms_notes = {"A": [], "B": [], "C": []}

    # Display the frame
    cv2.imshow("Paper Piano", frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
