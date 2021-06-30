# Face-Expression-Recognition-System

Face Emotion Recognition Project is developed using Opencv + Python bindings. The project uses "face_recognition" dlib library trained on deep learning. Frames are streamed directly from the raspberry pi(client) to the server using "imagezmq" python library which is based on 'zmq' protocol. An encoding file(encoding.pickle) which contains the encodings of the faces of persons has to be stored before hand. Frame processing that is encoding each incoming frame and comparing that encoding with the already stored encoding of the faces takes place on the server side. The frame containing the faces is analyzed by the model (classifier in our case) and their emotion is predicted accordingly. Livefeed is shown at last. Once the faces are recognized and the model predicts their emotion, a message (people_detected pickle file) is sent to the raspberry pi.

Based on this message, LED attached to the raspberry pi changes its color which shows the confirmation to the user that the face is recognized. The frames and message are exchanged between the raspberry pi and the server using the local network IP. Mutiple raspberry pi's can send their live feed at the same time to the server for face emotion recognition process.

## server.py
This is the server file where frames will be received and worked upon and hence the emotion of the person's face will be found.

## client.py
This file will run on raspberry pi. It will send the frames using camera module to the server. When the data will be received by raspberry pi, it will then turn on the respective led (blue, geen or red in our case) using the GPIO pins.

## CNN Model.py
This is the python file which is used for creating the model for predicting the emotion of a person's face.

## saved_model2.model
This is the model built using CNN file and is used for predicting emotions. It gives an accuracy of about 68%.
