import cv2
import numpy as np
import io
import picamera
import PlateExtraction
import OpticalCharacterRecognition

# Function to capture image using Pi camera
def capture_image():
    # Create a PiCamera object
    camera = picamera.PiCamera()

    # Capture an image
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg')
    data = np.frombuffer(stream.getvalue(), dtype=np.uint8)

    # Decode the image
    image = cv2.imdecode(data, 1)

    # Release the camera resources
    camera.close()

    return image

# Load the database file
def check_if_string_in_file(file_name, string_to_search):
    with open(file_name, 'r') as read_obj:
        for line in read_obj:
            if string_to_search in line:
                return True
    return False

# Capture image using Pi camera
image = capture_image()

# Perform plate extraction
plate = PlateExtraction.extraction(image)

# Perform OCR
text = OpticalCharacterRecognition.ocr(plate)
text = ''.join(e for e in text if e.isalnum())

print(text, end=" ")

# Check if the recognized text is in the database
if check_if_string_in_file('./Database/Database.txt', text) and text != "":
    print('Registered')
else:
    print("Not Registered")
