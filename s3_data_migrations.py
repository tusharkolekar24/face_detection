from io import BytesIO
import matplotlib.image as mpimg
import numpy as np
import boto3

# AWS Crediention
aws_access_key_id     = '<aws_access_key_id>'
aws_secret_access_key = '<aws_secret_access_key>'


def im_has_alpha(img_arr):
    h,w,c = img_arr.shape
    
    if c==4:
        out = True
    else:
         out = False
    return out

s3_client = boto3.client('s3', 
                      aws_access_key_id=aws_access_key_id, 
                      aws_secret_access_key=aws_secret_access_key
                      )

objects = s3_client.list_objects_v2(Bucket='main-bucket-images')

list_of_images = [obj['Key'] for obj in objects['Contents']]


#Creating Session With Boto3.
session = boto3.Session(
aws_access_key_id=aws_access_key_id,
aws_secret_access_key=aws_secret_access_key
)

#Creating S3 Resource From the Session.
s3 = session.resource('s3')

bucket      = s3.Bucket('main-bucket-images')
destbucket1 = s3.Bucket('no-transparent-pixels')
destbucket2 = s3.Bucket('transparent-pixels')


for image_name in list_of_images:
    extension = image_name.split('.')[-1]
    #print(image_name,extension)
    
    image_object = bucket.Object(image_name)
    image = mpimg.imread(BytesIO(image_object.get()['Body'].read()), extension)
    
    has_transparency = im_has_alpha(np.array(image))    
    
    #print(has_transparency,image_name,extension)
    
    if has_transparency == False:
        #Create a Soucre Dictionary That Specifies Bucket Name and Key Name of the Object to Be Copied
        copy_source = {
            'Bucket': 'main-bucket-images',
            'Key': image_name
        }

        destbucket1.copy(copy_source, image_name)
    else:
        #Create a Soucre Dictionary That Specifies Bucket Name and Key Name of the Object to Be Copied
        copy_source = {
            'Bucket': 'main-bucket-images',
            'Key': image_name
        }

        destbucket2.copy(copy_source, image_name)        

