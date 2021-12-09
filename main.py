import cv2 as cv
import numpy as np
from img_processing.procesado import filtrado, drawBox, detectarPunta
x,y = (0,0)
# Radio de la caja que se mostrara alrededor del punto del tracking.
r = 50
cap = cv.VideoCapture('BenderV2_luz.mp4')
tracker = cv.legacy_TrackerMOSSE.create()
while True:
    ret, frame = cap.read()
    blank = filtrado(frame)
    if(x+y == 0):
        x,y = detectarPunta(blank)
        # Hacer el rectangulo alrededor de las coords de la punta del cable.
        rect = (x - r // 2, y - r // 2, r, r)
        # Trackear la punta del cable.
        tracker.init(blank, rect)
    succes, bbox = tracker.update(blank)
    if succes:
        blank = drawBox(blank, bbox)
    else:
        cv.putText(img, "Lost", (75, 75), cv.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 1000), 2)
    cv.circle(blank,(x,y),10, 120,1)
    cv.imshow('con', blank)
    if cv.waitKey(1) == 27:
        exit(0)
