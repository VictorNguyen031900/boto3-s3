#shift + control + b to run script in atom with installed plugin
#1. check if montioring folder is created, if not create response
#2. check if connected to aws s3 Bucket
#3. tell user they can now drag and drop items into montioring folder to upload
#4.
import logging
import boto3
import json
import os
from botocore.exceptions import ClientError

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
    response = response['Contents']
    print(f"Objects in '{BUCKET_NAME}'")
    i = 0
    for x in response:
        i += 1
        print(str(i) + "." + x["Key"])
    print("You can now upload to the bucket! Drag and drop file into 'Upload' folder")
    # input("Press enter to continue...")
    ##this is where you implement a loop to go through the file directory and upload each file one by one and move to done folder
    if len(os.listdir(f'{currentDir}\\Upload\\')) == 0:
        print("There's nothing in the 'Upload' folder!  Please check again!")
    else:
        for file in os.listdir(f'{currentDir}\\Upload\\'):
            #print(file)
            fileAfter = f'Upload/{file}'
            s3.upload_file(fileAfter, BUCKET_NAME, file)
            print(f'{file} uploaded successfully')

    response = s3.list_objects(Bucket = BUCKET_NAME) #Getting objects from bucket
    response = response['Contents']
    print(f"UPDATED Objects in '{BUCKET_NAME}'")
    i = 0
    for x in response:
        i += 1
        print(str(i) + "." + x["Key"])


#Uploads dumb shit
# filename = 'Test/Ez.png'
# s3.upload_file(filename,'cs446project4', "hi.png")

if __name__ == "__main__":
    main()
