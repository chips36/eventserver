import base64
import datetime
import io
import json
import os
import random
import warnings

import cv2
import numpy as np
import requests
from PIL import Image
from deepface import DeepFace
from django.http import HttpResponse, JsonResponse
from nudenet import NudeDetector

warnings.filterwarnings("ignore", category=UserWarning)


# index
def index(request):
    return HttpResponse("SCF_EventServer ON")


# Take in base64 string and return cv image
def string2rgb(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    img = Image.open(io.BytesIO(imgdata))
    opencv_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    return opencv_img


def face_emotion(request):
    response = {}

    backends = [
        'opencv',
        'ssd',
        'dlib',
        'mtcnn',
        'retinaface',
        'mediapipe'
    ]

    if request.method == 'POST':
        request_data = json.loads(request.body)
        response = request_data

        request_time = datetime.datetime.now()
        #print(request.method, request_time, request_data)

        if len(request_data['img']) > 0:
            result = DeepFace.analyze("data:image/jpeg;base64," + request_data['img'],
                                      actions=['emotion'],
                                      detector_backend=backends[3], enforce_detection=False)

        print(result)
        if result[0]['emotion']:

            jpg_original = base64.b64decode(request_data['img'])
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            img = cv2.imdecode(jpg_as_np, flags=1)

            for data in result:

                if data['region']['x'] == '0' and data['region']['y'] == '0': continue

                cropped_img = img[data['region']['y']: data['region']['y'] + data['region']['h'],
                              data['region']['x']: data['region']['x'] + data['region']['w']]

                data["face_img"] = base64.b64encode(cv2.imencode('.jpg', cropped_img)[1]).decode()

            response['result'] = result

            # guid , 포함하여 서버로 전송         # POST (JSON)
            headers = {'Content-Type': 'application/json; chearset=utf-8'}
            #res = requests.post('http://192.168.0.27:8088/face/result', data=json.dumps(response),
            res = requests.post('http://DESKTOP-UV7J38L.iptime.org:8088/face/result', data=json.dumps(response),
                        headers=headers)
            print(str(res.status_code) + " | " + res.text)

        return JsonResponse(response)


def nude_detect(request):
    # global gDetector
    response = {}
    if request.method == 'POST':

        print(" ########################## NUDE CHECK  ########################## ")
        request_data = json.loads(request.body)
        request_time = datetime.datetime.now()
        # print(request.method, request_time, request_data)

        if len(request_data['img']) > 0:
            img = Image.open(io.BytesIO(base64.decodebytes(bytes(request_data['img'], "utf-8"))))

            suffix = datetime.datetime.now().strftime('%y%m%d_%H%M%S%f_')
            fileName = suffix + str(random.randint(1, 1000)) + '.jpg'

            img.save(fileName)

            detector = NudeDetector('base')
            result = detector.detect(fileName)
        # print(result)

        response = request_data
        response['result'] = result

        if len(result) > 0:

            # guid , 포함하여 서버로 전송
            # POST (JSON)
            headers = {'Content-Type': 'application/json; chearset=utf-8'}
            res = requests.post('http://DESKTOP-UV7J38L.iptime.org:8088/porno/result', data=json.dumps(response),
            #res=requests.post('http://192.168.0.27:8088/porno/result', data=json.dumps(response),
                                headers=headers)
            print(str(res.status_code) + " | " + res.text)

            for data in result:
                print(data)

        else:
            print("====> ############ NOT NUDE ##############")

        if os.path.exists(fileName):
            os.remove(fileName)

    return JsonResponse(response, safe=False)
