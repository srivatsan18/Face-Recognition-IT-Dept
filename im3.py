import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from tkinter import *
#top = Tk()
#top.title("SRM Attendance System")
#top.geometry("500x500")
#label=Label(top,text="Attendance System using Face Recognition",relief=RAISED)
#img=PhotoImage(file='srmlogo.png')
#Label(top,image=img).pack()
#label.pack()
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
#fourcc = cv2.VideoWriter_fourcc(*'MJPG') 
#out = cv2.VideoWriter('output4.avi', fourcc, 20.0, (640, 480))
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
    print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
nameList=[]
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                nameList.append(name)
                #lab=Label(top,text="hi")
                #lab.pack()
                print(name,'is appeared')
                now = datetime.now()
                dtday=now.strftime('%Y-%m-%d')
                dt=datetime.today()
                day=dt.day
                month=dt.month
                year=dt.year
		#dayy= datetime.datetime.today()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtday},{dtString},Present')
encodeListKnown = findEncodings(images)
print('Encoding Complete')
cap = cv2.VideoCapture(0)
 
while True:
    success, img = cap.read()
    #img = captureScreen()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)
        if faceDis[matchIndex]< 0.50:
            name = classNames[matchIndex].upper()
            markAttendance(name)
        else: 
            name = 'Unknown'
            # if(name=='Unknown'):
                # name=input('Enter your name:')
                # cv2.imwrite("ImagesAttendance/"+name+".jpg",img)
                # markAttendance(name)
                
        #print(name)
        y1,x2,y2,x1 = faceLoc
        y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
        cv2.rectangle(img,(x1,y2-35),(x2+10,y2),(0,255,0),cv2.FILLED)
        cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        #out.write(img)
    cv2.imshow('Webcam',img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        stream = os.popen('python emailsender.py')
        output = stream.read()
        print('********Email Sent*******')
        output
        break
cap.release()
#out.release()
cv2.destroyAllWindows()
#top.mainloop()


