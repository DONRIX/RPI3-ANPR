import cv2


from PlateExtractionmod import extraction1
from OpticalCharacterRecognition import ocr
from OpticalCharacterRecognition import check_if_string_in_file

image = cv2.imread('./CarPictures/mycar1.jpg')
plate = extraction1(image)
cv2.imshow('frame',plate)
text = ocr(plate)
text = ''.join(e for e in text if e.isalnum())
print(text, end=" ")
if check_if_string_in_file('./Database/Database.txt', text) and text != "":
    print('Registered')
    
else:
    print("Not Registered")
