#!/usr/bin/python3

from picamera import PiCamera
from time import sleep
import cv2
from PlateExtractiondef import extraction
from PlateExtractionmod import extraction1
from OpticalCharacterRecognition import ocr, check_if_string_in_file
import requests
from datetime import datetime
import os
from rpi_lcd import LCD
from signal import signal, SIGTERM, SIGHUP, pause

# Replace with your ThingSpeak API key
API_KEY = "G353563535636RIYAQ3"
# Replace with your ThingSpeak channel ID
CHANNEL_ID = "53353535"
# URL for sending data to ThingSpeak
BASE_URL = "https://api.thingspeak.com/update"

def capture_image(file_name):
    camera = PiCamera()
    camera.resolution = (1280, 720)  # Set the desired resolution
    camera.start_preview()
    sleep(2)  # Wait for the camera to warm up
    camera.capture(file_name)
    camera.stop_preview()



def main():
    # Initialize LCD
    

    # Display welcome message on LCD
    lcd.text("Scanning Plate..", 2)

    # Capture image using Raspberry Pi camera and assign a unique name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_name = f"car_image_{timestamp}.jpg"
    image_path = os.path.join("./CarPictures", image_name)
    #capture_image(image_path)

    # Load the captured image
    image = cv2.imread('/home/donrix/Desktop/Automatic-Number-Plate-Recognition-with-Raspberry-Pi/CarPictures/mycar1.jpg')

    # Perform plate extraction and OCR
    plate = extraction(image)

    # Check if plate extraction was successful and plate dimensions are valid
    if plate is not None and plate.shape[0] > 0 and plate.shape[1] > 0:
        # Display the extracted plate
        #cv2.imshow('frame', plate)
        lcd.text("Plate Found", 1)
        lcd.text("Extracting info....", 2)
        
        # Extract text from the plate
        text = ocr(plate)
        text = ''.join(e for e in text if e.isalnum())

        if text:
            details = text + "         "
            if check_if_string_in_file('/home/donrix/Desktop/Automatic-Number-Plate-Recognition-with-Raspberry-Pi/Database/Database.txt', text):
                print('Registered')
                details += "Registered"
                print(details)
            else:
                print("Not Registered1")
                details += "Not Registered"
                print(details)
        else:
            # Perform another plate extraction and OCR if the first one fails
            plate1 = extraction1(image)
            if plate1 is not None and plate1.shape[0] > 0 and plate1.shape[1] > 0:
                #cv2.imshow('frame', plate1)
                # Extract text from the plate
                text = ocr(plate1)
                text = ''.join(e for e in text if e.isalnum())
                if text:
                    details = text + "         "
                    if check_if_string_in_file('/home/donrix/Desktop/Automatic-Number-Plate-Recognition-with-Raspberry-Pi/Database/Database.txt', text):
                        print('Registered')
                        details += "Registered"
                        print(details)
                    else:
                        print("Not Registered2")
                        details += "Not Registered"
                        print(details)
                else:
                    print("No text detected on plate")
                    details = "No text detected on plate"
            else:
                print("Second extraction failed or no license plate detected!")
                details = "Second extraction failed or no license plate detected!"
            print(details)
    else:
        print("Plate extraction failed or invalid plate dimensions")
        details = "Plate extraction failed or invalid plate dimensions"

    # Send data to ThingSpeak
    try:
        # Get the current timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        # Create the payload with the API key, data, and timestamp
        payload = {
            "api_key": API_KEY,
            "status": f"{details} ({timestamp})"  # Use "status" to display data as text
        }
        # Send the data to ThingSpeak
        response = requests.post(BASE_URL, params=payload)
        response.raise_for_status()
        print("Data sent to ThingSpeak successfully!")
    except requests.exceptions.RequestException as e:
        print("Error sending data to ThingSpeak:", e)
        

    def safe_exit(signum, frame):
        exit(1)

    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        
        first_line = details[:16]
        second_line = details[16:]

        lcd.text(first_line, 1)
        lcd.text(second_line, 2)

        # Wait for 20 seconds before running the program again
        sleep(20)
        lcd.clear()
        lcd.text("Scanning again..", 1)
        sleep(2)
        main()

        

    finally:
        lcd.clear()


lcd = LCD()
lcd.text("Welcome!(^_^)", 1)
lcd.text("RaspbyPi 3 ANPR", 2)
sleep(3)




if __name__ == "__main__":
    main()
