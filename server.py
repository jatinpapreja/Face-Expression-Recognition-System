''' SERVER CODE '''

import socket
import face_recognition
import imagezmq
import pickle
import cv2 as cv
from keras.models import load_model
from keras.preprocessing.image import img_to_array
import numpy as np

TCP_IP = '192.168.43.142'     # server's ip address
TCP_PORT = 12345

''' creating a socket object'''
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((TCP_IP,TCP_PORT))
s.listen()

imagehub = imagezmq.ImageHub()          # this is created for receiving frames from raspberry pi

'''encodings.pickle file is loaded for detecting the known faces.'''
data = pickle.loads(open('encodings.pickle','rb').read())
people_detected = []
names = []

class_labels = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprise'}
emotion_color = {'Angry':(0,0,255),'Disgust':(0,255,0),'Fear':(255,255,255),'Happy':(255,255,0),'Neutral':(128,120,200),
                 'Sad':(255,0,0),'Surprise':(128,0,128)}

classifier = load_model('saved_model2.model')    # pre built model used
print('Everything connected..')

while True:
    (rpiName,frame) = imagehub.recv_image()     # receiving frame from pi
    imagehub.send_reply(b'OK')
    # cv.imshow("Livefeed",frame)
    rgb_frame = frame[:, :, ::-1]           # converting frame from bgr to rgb

    face_loc = face_recognition.face_locations(rgb_frame,model='hog')           # finding face locations
    face_encode = face_recognition.face_encodings(rgb_frame,face_loc)           # finding face encodings
    # print(face_encode)
    for face_encoding in face_encode:

        matches = face_recognition.compare_faces(data['encodings'],face_encoding,0.4)
        name = "Unknown"
        # print(matches)
        if True in matches:

            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

            people_detected.append('Detected')

        elif name == "Unknown":
            people_detected.append('Unknown')


        names.append(name)

    if len(face_loc)==0:
        people_detected.append('No Face detected')

    else:
        for ((top, right, bottom, left), name) in zip(face_loc, names):
            '''finding the face in frame and reshaping it according to input for classifier'''
            image = rgb_frame[top:bottom, left:right]
            image = cv.resize(image, (64, 64), interpolation=cv.INTER_AREA)
            image = image.astype("float") / 255.0
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)

            '''Predicting the emotion'''
            pred = classifier.predict(image)
            pred = pred.argmax(axis=1)[0]
            # print(pred)
            label = class_labels[pred]
            #print(label)

            '''draw the predicted face name on the image'''
            cv.rectangle(frame, (left, top), (right, bottom), emotion_color[label], 2)
            y1 = top - 15 if top - 15 > 15 else top + 15
            y2 = bottom+15
            cv.putText(frame, name, ((left+right)//2, y1), cv.FONT_HERSHEY_SCRIPT_COMPLEX,
                        0.75, (128,10,255), 2)
            cv.putText(frame, label, ((left + right) // 2, y2), cv.FONT_HERSHEY_SCRIPT_COMPLEX,
                       0.75, emotion_color[label], 2)

    cv.imshow('Livefeed',frame)     # Livefeed is shown here.

    key = cv.waitKey(1) & 0xFF

    '''For quiting'''
    if key == ord('q'):
        people_detected.append('EXIT')
        s.listen()
        conn, addr = s.accept()
        data_string = pickle.dumps(people_detected)
        conn.send(data_string)
        break

    '''Data is being sent to raspberry pi(client)'''
    s.listen()
    conn,addr = s.accept()
    data_string = pickle.dumps(people_detected)
    conn.send(data_string)
    people_detected = []
    names = []








