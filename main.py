import cv2
import tensorflow as tf
import numpy as np
import keras.utils as image
import tensorflow_addons as tfa


# Load the model
with tf.keras.utils.custom_object_scope({'CohenKappa': tfa.metrics.CohenKappa(num_classes=4)}):
    model = tf.keras.models.load_model("C:/Users/malit/Downloads/my_trained_model3.h5")

# Create a VideoCapture object to capture images from the camera
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
        # Convert the captured frame to a format that can be used by the model
        img = cv2.resize(frame, (300, 300))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = img / 255.0  # normalize the pixel values

        # Classify the image using the trained model
        classes = model.predict(img, batch_size=10)[0]
        class_label = np.argmax(classes)

        # Map the class label to the corresponding class name
        if class_label == 0:
            print("Person is Happy")
        elif class_label == 1:
            print("Person is Sad")
        elif class_label == 2:
            print("Person is Angry")
        else:
            print("Person is Neutral")

# Release the resources
cap.release()
cv2.destroyAllWindows()


