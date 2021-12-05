import cv2 as cv
import numpy as np

def drawBox(img, bbox):
  x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
  return cv.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)

def filtrado(img):
    blank = np.zeros(img.shape, dtype='uint8')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = 255 - gray
    cv.imshow('a', gray)
    mediana = cv.medianBlur(gray, 25)
    ret, thresh = cv.threshold(mediana, 160, 255, cv.THRESH_BINARY)
    cv.imshow('t', thresh)
    contorno, j = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    cv.drawContours(blank, contorno, -1, (255, 255, 255), 1)
    gris = cv.cvtColor(blank, cv.COLOR_BGR2GRAY)
    return gris

def detectarPunta(gris):
    for y,pixel in enumerate(gris):
        s = pixel.nonzero()[0]
        if(len(s) > 0):
            x = s[0]
            r = 50
            break
    return (x,y)
cap = cv.VideoCapture('http://169.254.241.82:8080/?action=stream')
tracker = cv.legacy_TrackerMOSSE.create()
x = 0
y = 0
while True:
    ret, frame = cap.read()
    blank = filtrado(frame)
    if(x+y == 0):
        x,y = detectarPunta(blank);
        rect = (x - r // 2, y - r // 2, r, r)
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
