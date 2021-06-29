import cv2
import mediapipe as mp
import time
import numpy as np
import handmodule as htm

cap = cv2.VideoCapture(0)

detector = htm.detecthand(detectc=0.75)
tipId = [4,8,12,16,20]
while True:
    ret,frame = cap.read()
    frame = detector.track(frame)
    lmlist = detector.findpos(frame,draw=False)

    # here we need to get the landmark points of tips of our fingers namely 4,8,12,16,20
    #if those are below 2,6,10,14,18 respectively then we will assume that they are closed
    if len(lmlist)!=0:
        #demo
        #if lmlist[8][2] < lmlist[6][2]:
        #    print("open")
        # else:
        #     print("close")
        fingers = []
        if lmlist[tipId[0]][1] > lmlist[tipId[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
            #we write seperate code for thumb...so 1,5
            if lmlist[tipId[id]][2] < lmlist[tipId[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)

        numoffing = fingers.count(1)#counts the number of 1s in the list
        print(numoffing)
        cv2.putText(frame,f'count:{numoffing}',(10,60),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
        #for thunb its a problem so its better if we take reference with the -1 point's left and right
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0XFF==27:
        break
cap.release()
cv2.destroyAllWindows()