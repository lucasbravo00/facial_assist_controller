import cv2
import face_recognition as fr
import os
import numpy as np
from datetime import datetime

# Create database
path = 'Employees'
my_images = []
employee_names = []
employee_list = os.listdir(path)

for name in employee_list:
    current_image = cv2.imread(path + '/' + name)
    my_images.append(current_image)
    employee_names.append(os.path.splitext(name)[0])


# Encode images
def encode(images):
    # List of encoded images
    encoded_list = []

    for image in images:
        # Convert images to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Encode and add to the list
        encoded = fr.face_encodings(image)[0]
        encoded_list.append(encoded)

    return encoded_list


# Register entries
def register_entry(person):
    f = open('log.csv', 'r+')
    data_list = f.readlines()
    registered_names = []

    for line in data_list:
        entry = line.split(',')
        registered_names.append(entry[0])

    if person not in registered_names:
        now = datetime.now()
        now_string = now.strftime('%H:%M:%S')
        f.writelines(f'\n{person}, {now_string}')


encoded_images = encode(my_images)

# Capture an image from the webcam
capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Read the camera image
success, image = capture.read()

if not success:
    print('Failed to capture the image')
else:
    # Recognize face in the capture
    captured_face = fr.face_locations(image)

    # Encode captured face
    captured_face_encoded = fr.face_encodings(image, captured_face)

    # Search for matches
    for encoded_face, face_location in zip(captured_face_encoded, captured_face):
        matches = fr.compare_faces(encoded_images, encoded_face)
        distances = fr.face_distance(encoded_images, encoded_face)
        match_index = np.argmin(distances)

        if distances[match_index] > 0.6:
            print('You do not match any of our employees')
        else:
            name = employee_names[match_index]

            # Face coordinates
            y1, x2, y2, x1 = face_location

            # Draw rectangle around the face
            cv2.rectangle(image, (x1, y1), (x2, y2), (175, 200, 0), 2)

            # Determine dynamic font size
            font_scale = 1  # Base size
            thickness = 2  # Base thickness
            (text_width, text_height), baseline = cv2.getTextSize(name, cv2.FONT_HERSHEY_COMPLEX, font_scale, thickness)

            # Adjust name rectangle size based on text width
            while text_width > (x2 - x1):  # If text is larger than face, reduce size
                font_scale -= 0.1
                (text_width, text_height), baseline = cv2.getTextSize(name, cv2.FONT_HERSHEY_COMPLEX, font_scale,
                                                                      thickness)

            # Draw rectangle behind the name
            cv2.rectangle(image, (x1, y2 - text_height - 10), (x1 + text_width + 10, y2), (175, 200, 0), cv2.FILLED)

            # Draw the adjusted text inside the rectangle
            cv2.putText(image, name, (x1 + 5, y2 - 5), cv2.FONT_HERSHEY_COMPLEX, font_scale, (255, 255, 255), thickness)

            register_entry(name)

            # Display image
            cv2.imshow('Webcam Image', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
