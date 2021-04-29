# Importing all necessary libraries
import cv2
import os
import pafy
from time import sleep
import boto3
import datetime
from datetime import timezone

# Read the video from specified path
# cam = cv2.VideoCapture("C:\\Users\\Admin\\PycharmProjects\\project_1\\openCV.mp4")
url = "https://www.youtube.com/watch?v=oIBERbq2tLA"
video = pafy.new(url)
best = video.getbest(preftype="mp4")

s3 = boto3.resource('s3')
BUCKET = "bucketswen614"

# cam = cv2.VideoCapture(best.url)
try:
      
    # creating a folder named data
    if not os.path.exists('data'):
        os.makedirs('data')
  
# if not created then raise error
except OSError:
    print ('Error: Creating directory of data')
  
# frame
currentframe = 0
  
while(True):
    
    cam = cv2.VideoCapture(best.url)
    # reading from frame
    ret,frame = cam.read()
    cam.release()
    sleep(3)
    if ret:
        # if video is still left continue creating images

        # set filename for s3 bucket
        filename = f"""GOL_2000_{datetime.datetime.now(timezone.utc)}"""
        filename = filename.replace(" ", "____")
        filename = filename.replace(":", "___") 
        filename = filename.replace("+", "__") 


        print(filename)

        # set name of file
        name = './data/frame' + str(currentframe) + '.jpg'
        print ('Creating...' + name)
  
        # writing the extracted images
        cv2.imwrite(name, frame)
        
        # upload to bucket
        s3.Bucket(BUCKET).upload_file(name, filename)  

        # increasing counter so that it will
        # show how many frames are created
        currentframe += 1
    else:
        break
  
# Release all space and windows once done
cv2.destroyAllWindows()