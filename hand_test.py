import cv2
import mediapipe as mp
import serial
import time

arduino = serial.Serial('COM4', 9600) 
time.sleep(2) 

# MediaPipe setup
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_finger_str = ""

tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    if not success:
        continue

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    fingers = []

    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        lmList = []

        for id, lm in enumerate(handLms.landmark):
            h, w, _ = img.shape
            lmList.append((int(lm.x * w), int(lm.y * h)))

        # Thumb
        fingers.append(1 if lmList[tipIds[0]][0] 
                       > lmList[tipIds[0] - 1][0] else 0)

        # Other fingers
        for id in range(1, 5):
            fingers.append(1 if lmList[tipIds[id]][1] 
                           < lmList[tipIds[id] - 2][1] else 0)

      
        finger_str = ''.join(str(f) for f in fingers)
        print("Detected:", finger_str)
        if finger_str != prev_finger_str:
            arduino.write((finger_str + '\n').encode())
            prev_finger_str = finger_str

        mpDraw.draw_landmarks(img, handLms, 
                              mpHands.HAND_CONNECTIONS)

    cv2.imshow("Hand Tracking", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
