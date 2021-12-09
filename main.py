import cv2 as cv
import numpy as np
import math
from img_processing.procesado import filtrado, drawBox, detectarPunta, encontrar_y
from img_processing.calculos import calcular_angulo
x,y = (0,0)
x_ref = 0
# Radio de la caja que se mostrara alrededor del punto del tracking.
r = 50
#cap = cv.VideoCapture('BenderV2_no_luz.mp4')
cap = cv.VideoCapture('BenderV2_Luz.mp4')
#tracker = cv.legacy_TrackerMOSSE.create()
tracker = cv.TrackerCSRT.create()
while True:
    ret, frame = cap.read()
    if frame is None:
        break
    blank = filtrado(frame)
    if(x+y == 0):
        x,y = detectarPunta(blank)
        # Hacer el rectangulo alrededor de las coords de la punta del cable.
        rect = (x - r//2, y - r//2, r, r)
        # Trackear la punta del cable.
        y_ref = encontrar_y(blank) - 50 # -50 pixeles arriba para ajuste.
        tracker.init(blank, rect)
        x_ref = x
    succes, bbox = tracker.update(blank)
    if succes:
        blank = drawBox(blank, bbox)
        x = int(bbox[0])
        y = int(bbox[1])
    else:
        cv.putText(blank, "Lost", (75, 75), cv.FONT_HERSHEY_SIMPLEX, 0.7, (100, 255, 1000), 2)
        x,y = (0,0)
    cv.circle(blank,(x,y), 10, (0,0,255),1)
    cv.circle(blank,(x_ref,y_ref), 5, (0,255,0),1)
    cv.imshow('preview sensado', blank)
    angulo = print(calcular_angulo(x,y,x_ref,y_ref))
    if cv.waitKey(1) == 27:
        exit(0)
print("El video acabo o se perdio la conexion con el flujo de streaming")
