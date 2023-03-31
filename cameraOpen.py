import json

import cv2
import requests

cap = cv2.VideoCapture(0)

while True:

    # Read a frame from the camera
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('frame', frame)

    # Wait for the user to press 'q' to quit or 'c' to capture a frame
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        message = input("Enter a Message: ")
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", 'http://localhost:5000/post-example', headers=headers, data=json.dumps({'message': message}))
        print(response.json())
        response = requests.get('http://localhost:5000/')
        print(response.status_code)
        print(response.text)



