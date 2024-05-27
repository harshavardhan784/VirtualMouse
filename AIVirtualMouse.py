import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np

####################
wCam, hCam = 640, 480
frameR = 100 
screen_width, screen_height = pyautogui.size()
####################

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

hand_detector = mp.solutions.hands.Hands(max_num_hands = 1)
drawing_utils = mp.solutions.drawing_utils

# detector = htm.handDetector(maxHands = 1)

pTime = 0
while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    
 
    output = hand_detector.process(rgb_frame)
    
    hands = output.multi_hand_landmarks
    index_y = 0
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*wCam)
                y = int(landmark.y*hCam)
                
                # cv2.rectangle(frame, (frameR, frameR), (wCam - frameR, hCam - frameR), (255,0,255),2)
                
                if id == 8:
                    cv2.circle(frame, (x,y), 20, (255,0,255), cv2.FILLED)
                    # index_x, index_y = screen_width/wCam*x, screen_height/hCam*y
                    index_x = int(np.interp(x, (0,wCam),(0,screen_width)))
                    index_y = int(np.interp(y, (0,hCam),(0,screen_height)))
                    pyautogui.moveTo(index_x,index_y)
                
                if id == 12:
                    cv2.circle(frame, (x,y), 20, (255,0,255), cv2.FILLED)
                    # thumb_x, thumb_y = screen_width/wCam*x, screen_height/hCam*y
                    thumb_x = int(np.interp(x, (0,wCam),(0,screen_width)))
                    thumb_y = int(np.interp(y, (0,hCam),(0,screen_height)))
                    print("outside", abs(index_y- thumb_y))
                    if abs(index_y- thumb_y) <20:
                        print("click")
                        pyautogui.click()
                        pyautogui.sleep(1)
    
    cTime = time.time()      
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(frame, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2) 
    cv2.imshow("Virtual Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    