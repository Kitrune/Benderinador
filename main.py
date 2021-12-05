import cv2 as cv
import numpy as np

def drawBox(img, bbox):
  x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
  return cv.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)

def filtrado(img):
    # Iniciar una imagen vacia para poner relieves.
    blank = np.zeros(img.shape, dtype='uint8')
    # Convertir la imagen a escala de grises.
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Invertir los colores, para aplicar el threshold sobre numeros grandes.
    gray = 255 - gray
    # Aplicar el filtro de la mediana para resaltar mas los bordes del cable.
    mediana = cv.medianBlur(gray, 25)
    # Aplicar un threshold para solo quedarnos con las partes mas blancas de la imagen.
    ret, thresh = cv.threshold(mediana, 160, 255, cv.THRESH_BINARY)
    # Calcular el contorno de la imagen en threshold.
    contorno, j = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    cv.drawContours(thresh, contorno, -1, (255, 255, 255), 1)
    # Imagen con contornos del cable.
    return thresh

# Encuentra el pixel mas alto, que corresponde a la punta del cable.
def detectarPunta(gris):
    x,y = (0,0)
    # Buscar en cada columna de la imagen.
    for y,pixel in enumerate(gris):
        s = pixel.nonzero()[0]
        if(len(s) > 0):
            x = s[0]
            r = 50
            break
    return (x,y)
cap = cv.VideoCapture('http://169.254.241.82:8080/?action=stream')
tracker = cv.legacy_TrackerMOSSE.create()
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
