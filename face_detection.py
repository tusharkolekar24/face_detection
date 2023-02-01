#import library
import os
import cv2

# take input from user : File location where user want to store output and image path
print("Enter your Image Path:",'\nFormat of path:"D:\git_practice\face_detection\image_folder\g.jpg"\n')
input_image_path = input()
print('\n',"Enter your Image stored location:",'\nFormat of path:"D:\git_practice\face_detection\headshort_folder"\n')
input_directory_path = input()

# create folder to store output files.
updated_image_path = input_image_path[1:-1]
updated_directory_path = input_directory_path[1:-1]

#check 1st folder is exist or not.
if not os.path.exists(os.path.join(updated_directory_path,'process_image')):
    os.mkdir(os.path.join(updated_directory_path,'process_image'))
    
if not os.path.exists(os.path.join(updated_directory_path,'headshorts')):
    os.mkdir(os.path.join(updated_directory_path,'headshorts'))

# import model to dected face
#eye_dectector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# import file path of image
image = cv2.imread(updated_image_path)

#create image in to gray scales
gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# configure parameters like gray scale image,scalefactor and minneighbors 
results = face_detector.detectMultiScale(gray_img, scaleFactor=1.15,
                                         minNeighbors=2,minSize=(34,35), 
                                         flags=cv2.CASCADE_SCALE_IMAGE
                                        )

# draw rectangles on face which was detected our face detection model 
for cordinates in results:
    x,y,w,h = cordinates[0],cordinates[1],cordinates[2],cordinates[3]
    #print(cordinates)
    cv2.rectangle(image,(x,y),(x+w,y+h),(36,256,16),2)

# created folder and update with images
current_image = os.path.join(updated_directory_path,'process_image','{}.jpg'.format(updated_image_path.split('\\')[-1].split('.')[0]))
cv2.imwrite(current_image,image)


# created folder and update with headshort
counter = 0 
new_image = cv2.imread(updated_image_path)

for (x,y,w,h) in results:
    current_image = os.path.join(updated_directory_path,
                             'headshorts','{}_{}.jpg'.format(updated_image_path.split('\\')[-1].split('.')[0],counter))
    
    cv2.imwrite(current_image,new_image[y:y+h,x:x+w])
    counter+=1