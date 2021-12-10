import cv2 as cv
import numpy as np

def increase_brightness(img, value=30):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv.merge((h, s, v))
    img = cv.cvtColor(final_hsv, cv.COLOR_HSV2BGR)
    return img

def filtrado(img):
    # Iniciar una imagen vacia para poner relieves.
    blank = np.zeros(img.shape, dtype='uint8')
    # Aumenta el brillo de la imagen
    #img = increase_brightness(img,value=10)
    # Convertir la imagen a escala de grises.
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Invertir los colores, para aplicar el threshold sobre numeros grandes.
    gray = 255 - gray
    # Aplicar el filtro de la mediana para resaltar mas los bordes del cable.
    mediana = cv.medianBlur(gray, 25)
    # Aplicar un threshold para solo quedarnos con las partes mas blancas de la imagen.
    ret, thresh = cv.threshold(mediana, 165, 255, cv.THRESH_BINARY)
    # Calcular el contorno de la imagen en threshold.
    contorno, j = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
    cv.drawContours(blank, contorno, -1, (255, 255, 255), 1)
    # Imagen con contornos del cable.
    return blank

def drawBox(img, bbox):
  x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
  return cv.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 1)

# Encuentra el pixel mas alto, que corresponde a la punta del cable.
def detectarPunta(gris):
    x,y = (0,0)
    #gris = gris[100:-100]
    # Buscar en cada columna de la imagen.
    for y,pixel in enumerate(gris):
        pixel = pixel[0:-300]
        s = pixel.nonzero()[0]
        if(len(s) > 0):
            x = s[0]
            break
    return (x,y)
def encontrar_y(img):
    # Buscar el primer pixel de cada columnda de la imagen.
    for y, pixel in enumerate(img):
        # Buscar en los primeros 50 pixeles.
        pixel = pixel[0:25]
        for p in pixel:
            gris = np.mean(p)
            if(gris > 0):
                return y
