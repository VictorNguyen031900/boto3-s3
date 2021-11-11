#shift + control + b to run script in atom with installed plugin
#1. check if montioring folder is created, if not create response
#2. check if connected to aws s3 Bucket
#3. tell user they can now drag and drop items into montioring folder to upload
#4.
import logging
import boto3
import json
import os
import threading
import sys
import shutil

class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            print(f'{self._filename} {round((self._seen_so_far / 1000000), 2)}MB/{round((self._size / 1000000),2)}MB {round(percentage, 2)}%')

def main():
    currentDir = os.getcwd()

    print("Checking if there is an 'Upload' folder")
    if(os.path.isdir(currentDir+'\\Upload')):
        print("'Upload' folder detected!")
    else:
        print("'Upload' folder not detected, don't worry I'll make one :)")
        os.mkdir(f'{currentDir}\\Upload')
        print("There we go champ!")

    if(os.path.isdir(currentDir+'\\Done')):
        print("'Done' folder detected!")
    else:
        print("'Done' folder not detected, don't worry I'll make on :)")
        os.mkdir(f'{currentDir}\\Done')
        print("There we go champ!")

    BUCKET_NAME = 'cs446project4'

    s3 = boto3.client('s3')

    response = s3.list_buckets()
    # print(response['Buckets'])
    # a = []
    # for x in response['Buckets']:
    #     print(x["Name"])
    #     a.append(x["Name"])
    # j = 1
    # for i in a:
    #     print(str(j) + ". " + i)
    #     j += 1

    response = s3.list_objects(Bucket = BUCKET_NAME) #Getting objects from bucket
    # print(response)
    try:
        response = response['Contents']
        print(f"Objects in '{BUCKET_NAME}'")
        i = 0
        for x in response:
            i += 1
            print(str(i) + "." + x["Key"] + " [SIZE]: " + convertMetric(x["Size"]) + " [LINK]: " + s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': x["Key"]}, ExpiresIn=3600))
    except:
        print(f'{BUCKET_NAME} is empty!')

    print("You can now upload to the bucket! Drag and drop file into 'Upload' folder")
    input("Press enter to continue...")
    ##this is where you implement a loop to go through the file directory and upload each file one by one and move to done folder
    if len(os.listdir(f'{currentDir}\\Upload\\')) == 0:
        print("There's nothing in the 'Upload' folder!  Please check again!")
    else:
        for file in os.listdir(f'{currentDir}\\Upload\\'):
            #print(file)
            fileAfter = f'Upload/{file}'
            s3.upload_file(fileAfter, BUCKET_NAME, file, Callback = ProgressPercentage(fileAfter))
            print(f'{file} uploaded successfully')
            shutil.move(fileAfter,f'Done/{file}')
            print(f"Moved file '{file}' to 'Done' folder!")

    try:
        response = s3.list_objects(Bucket = BUCKET_NAME)
        response = response['Contents']
        print(f"UPDATED Objects in '{BUCKET_NAME}'")
        i = 0
        for x in response:
            i += 1
            print(str(i) + "." + x["Key"] + " [SIZE]: " + convertMetric(x["Size"]) + " [LINK]: " + s3.generate_presigned_url('get_object', Params={'Bucket': BUCKET_NAME, 'Key': x["Key"]}, ExpiresIn=3600))
    except:
        print(f'{BUCKET_NAME} is empty!')

    # response = s3.list_objects(Bucket = BUCKET_NAME) #Getting objects from bucket
    # response = response['Contents']
    # print(f"UPDATED Objects in '{BUCKET_NAME}'")
    # i = 0
    # for x in response:
    #     i += 1
    #     print(str(i) + "." + x["Key"])

def convertMetric(number):
    return (f"{round((number/1000000),2)} MB")

#Uploads dumb shit
# filename = 'Test/Ez.png'
# s3.upload_file(filename,'cs446project4', "hi.png")

if __name__ == "__main__":
    main()
