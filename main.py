import cv2 as cv
import socket
from img_processing.procesado import filtrado, drawBox, detectarPunta, encontrar_y
from img_processing.calculos import calcular_angulo
setpoint = 45
x,y = (0,0)
x_ref = 0
accion = b'0'
# Radio de la caja que se mostrara alrededor del punto del tracking.
r = 50
#cap = cv.VideoCapture('BenderV2_no_luz.mp4')
cap = cv.VideoCapture('BenderV2_Luz.mp4')
#cap = cv.VideoCapture('http://raspberrypi.local:8080/?action=stream')
#tracker = cv.legacy_TrackerMOSSE.create()
tracker = cv.TrackerCSRT.create()

# Conexion TCP
PORT = 22333
hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)
print("IP:", IP, ", Puerto:",PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((IP,PORT))
s.listen(1)
conn, addr = s.accept()
conn.setblocking(0)
# Conexion TCP establecida
while True:
    # ---
    # Procesado de imagen
    # ---
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
        x = int(bbox[0])+r//2
        y = int(bbox[1])+r//2
    else:
        cv.putText(blank, "Lost", (75, 75), cv.FONT_HERSHEY_PLAIN, 0.7, (100, 255, 1000), 2)
        x,y = (0,0)
    angulo = calcular_angulo(x,y,x_ref,y_ref)

    # ---
    # Ordenes al motor a pasos
    # ---

    # Se alcanzo el setpoint?
    if(angulo >= setpoint):
        # Si, Entonces el motor queda en standby
        accion = b'0' 
    else:
        # No, entonces el motor avanza un poco
        accion = b'1'

    # Se envia la orden al motor
    try:
        data = conn.recv(3)
        print("Enviando ordenes a motor")
        conn.sendall(accion)
    except BlockingIOError:
        # El motor esta ocupado, por lo que no puede recibir ordenes
        print("Motor ocupado")

    # ---
    # Graficos
    # ---

    # linea del la punta al punto de referencia
    cv.line(frame,(x,y),(x_ref,y_ref),(255,0,0),2)
    # linea de referencia
    cv.line(frame,(x_ref,80),(x_ref,y_ref),(150,0,0),2)
    # Punto en la punta
    cv.circle(frame,(x,y), 5, (0,0,255),10)
    # Punto en la referencia
    cv.circle(frame,(x_ref,y_ref), 5, (0,255,0),10)
    # Texto del angulo
    cv.putText(frame, f"{angulo:.2f} grados", (x_ref + 20, y_ref), cv.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)
    cv.imshow('preview sensado', frame)
    
    if cv.waitKey(1) == 27:
        conn.close()
        exit(0)
print("El video acabo o se perdio la conexion con el flujo de streaming")
