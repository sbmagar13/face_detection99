import logging
import boto3
# from botocore.exceptions import ClientError
import json

# import math
# import matplotlib.pyplot as plt


configfile = 'credentials_config.txt'
with open(configfile) as cf:
    lines = cf.read().splitlines()
    access_key_id = lines[0]
    secret_access_key = lines[1]
    session_token = lines[2]


session = boto3.session.Session(profile_name = 'default')
client1 = session.client('rekognition', aws_access_key_id=access_key_id,
                      aws_secret_access_key=secret_access_key, aws_session_token=session_token, region_name='us-east-1')


client2 = session.client('s3', aws_access_key_id=access_key_id,
                      aws_secret_access_key=secret_access_key, aws_session_token=session_token, region_name='us-east-1')


def get_image(filename):
    with open(filename, 'rb') as imgfile:
        return imgfile.read()


# def detect_images(images):
#     fig=plt.figure(figsize=(40,40))
#     rows = math.ceil((len(images))/4)
#     columns = math.ceil(len(images)/rows)
#     for i in range(0, columns*rows):
#         ax = fig.add_subplot(rows, columns, i+1)
#         ax.xaxis.set_visible(False)
#         ax.yaxis.set_visible(False)
#         if i < len(images):
#             plt.imshow(images[i])
#     plt.tight_layout()
#     plt.show


imgb = get_image("Images/ramailo.jpg")
res1 = client1.detect_faces(
    Image={
        'Bytes':imgb
    },
    Attributes=['ALL']
)
for person in res1['FaceDetails']:
    # print(json.dumps(face, indent=4))
    print('Gender: ' + person['Gender']['Value'] )
    print('Age Range: ' + '{}-{}'.format(person['AgeRange']['Low'], person['AgeRange']['High']))
    for attr in person['Emotions']:
        if attr['Confidence'] > 55.70:
            print('Emotion of state: ' + attr['Type'])
    if person['Eyeglasses']['Value'] == True:
        print('- Wearing eyeglasses. And its ' + '{:.2f}'.format(person['Eyeglasses']['Confidence']) + '% sure.')
    if person['Sunglasses']['Value'] == True:
        print('- Wearing sunglasses. And its ' + '{:.2f}'.format(person['Sunglasses']['Confidence']) + '% sure.')
    if person['Beard']['Value'] == True:
        print('- Has Beard.')
    if person['Mustache']['Value'] == True:
        print('- Has Mustache.')

    print ('-----------------------------------')



res2 = client2.list_buckets()
print('Existing Buckets:')
for bucket in res2['Buckets']:
    print(f'  {bucket["Name"]}')



# upload file in bucket:
#
# with open('PAS072BCT638.jpg', 'rb') as f:
#     data = f.read()
# res3 = client2.put_object(
#     ACL='private',
#     Body=data,
#     Bucket='rekognitiondata99',
#     Key='PAS072BCT638.jpg',
# )
# print('Uploaded successfully!')
