''' CLIENT CODE '''

from imutils.video import VideoStream
import imagezmq
import socket
import time
import RPi.GPIO as GPIO
import os
import pickle



TCP_IP = "192.168.43.142"       # server's ip address
TCP_PORT = 8882
Message = 'Detect'


print("DONE.....")
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23,GPIO.OUT)  #blue light
GPIO.setup(24,GPIO.OUT)  #green light
GPIO.setup(25,GPIO.OUT)  #red light



def output_rasp(data1):
    if data1 == "Detected":
        GPIO.output(23,GPIO.LOW)
        GPIO.output(24,GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(24,GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(24,GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(24,GPIO.LOW)
    elif data1=="Unknown":
        GPIO.output(23, GPIO.LOW)
        GPIO.output(25, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(25, GPIO.LOW)
        time.sleep(0.2)
        GPIO.output(25, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(25, GPIO.LOW)
    elif data1=="No Face detected":
        pass
    GPIO.output(23,GPIO.HIGH)

sender = imagezmq.ImageSender(connect_to="tcp://"+TCP_IP+":5555")
print("Connected")

rpiName = "raspberry pi"
vs = VideoStream(usePiCamera=True,resolution=(640,480),framerate=40).start()
time.sleep(2.0)
GPIO.output(23,GPIO.HIGH)
exit_flag = 0
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    frame = vs.read()
    sender.send_image(rpiName,frame)
    s.send(Message.encode())
    data1 = s.recv(4096)
    data_arr = pickle.loads(data1)
    for elem in data_arr:
        if elem=="EXIT":
            GPIO.output(23, GPIO.LOW)
            exit_flag = 1
            break
        output_rasp(elem)

    if exit_flag==1:
        break


GPIO.output(23,GPIO.LOW)
os.system('sudo shutdown now -h')