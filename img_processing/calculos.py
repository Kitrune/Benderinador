from math import atan, degrees
def calcular_angulo(x1 : int, y1 : int, x2 : int, y2 : int):
    cateto_opuesto = abs(y1 - y2)
    cateto_adyacente = abs(x1 - x2)
    tan = cateto_opuesto/cateto_adyacente
    return degrees(atan(tan))
