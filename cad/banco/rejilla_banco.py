"""Gavia, rejilla del banco de empuje para corte láser.

Dibuja en 2D la rejilla de flejes del aro final (gavia_aro.py) para cortarla en acrílico de 6 mm:
flejes paralelos con ranura de 5 mm, cinco nervios y un aro perimetral. Los parámetros se leen de
gavia_aro.py, así que si cambian allá cambian acá. No necesita Blender ni librerías.

    python rejilla_banco.py

Escribe rejilla_banco.svg y rejilla_banco.dxf (en mm) y anota las medidas de la tira del ducto.
"""
import ast
import math
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPT_ARO = os.path.join(AQUI, "..", "blender", "gavia_aro.py")
HOLGURA_MONTAJE = 0.0003  # el disco entra en el ducto con 0,3 mm de juego por lado
AREA_MIN_MM2 = 15.0  # las ranuras más chicas que esto, contra el aro, quedan llenas (astillas frágiles)
SOLAPE_DUCTO = 0.020  # solape pegado de la tira de policarbonato
ESPESOR_TIRA = 0.001  # policarbonato de 1 mm


def parametros():
    """Lee el diccionario de P.update({...}) de gavia_aro.py sin ejecutar Blender."""
    arbol = ast.parse(open(SCRIPT_ARO, encoding="utf-8").read())
    for nodo in ast.walk(arbol):
        if (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Attribute)
                and nodo.func.attr == "update"):
            return ast.literal_eval(nodo.args[0])
    raise RuntimeError("no encontré P.update en gavia_aro.py")


def recortar(poligono, limite):
    """Sutherland-Hodgman: recorta un polígono convexo contra otro convexo (antihorario)."""
    salida = poligono
    for i in range(len(limite)):
        a, b = limite[i], limite[(i + 1) % len(limite)]
        adentro = lambda p: (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]) >= 0
        entrada, salida = salida, []
        for j in range(len(entrada)):
            p, q = entrada[j], entrada[(j + 1) % len(entrada)]
            if adentro(q):
                if not adentro(p):
                    salida.append(cruce(a, b, p, q))
                salida.append(q)
            elif adentro(p):
                salida.append(cruce(a, b, p, q))
        if not salida:
            return []
    return salida


def cruce(a, b, p, q):
    x1, y1, x2, y2 = a[0], a[1], b[0], b[1]
    x3, y3, x4, y4 = p[0], p[1], q[0], q[1]
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def area(pol):
    return abs(sum(pol[i][0] * pol[(i + 1) % len(pol)][1] - pol[(i + 1) % len(pol)][0] * pol[i][1]
                   for i in range(len(pol)))) / 2


def circulo(r, n=360):
    return [(r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def rejilla(P):
    """Contorno exterior y ranuras, en mm, con el mismo trazado que L.rejilla_fleje."""
    r_hel = P["helice_pulg"] * 0.0254 / 2
    r_in = r_hel + P["holgura_punta"]  # cara interior del liner
    radio = r_in - HOLGURA_MONTAJE
    paso, esp = P["abertura_rejilla"], P["fleje_espesor"]
    esp_nervio = esp * 1.3
    aro = 0.004
    r_libre = radio - aro  # adentro del aro perimetral
    # bordes de los flejes (en y) y de los nervios (en x), como en gavia_lib.rejilla_fleje
    p = paso + esp
    n = int(radio / p)
    flejes = [i * p for i in range(-n, n + 1)]
    nervios = [-radio + 2 * radio * (k + 1) / (P["nervios_rejilla"] + 1)
               for k in range(P["nervios_rejilla"])]
    franjas_y = [(flejes[i] + esp / 2, flejes[i + 1] - esp / 2) for i in range(len(flejes) - 1)]
    cortes_x = [-radio] + nervios + [radio]
    franjas_x = [(cortes_x[0], cortes_x[1] - esp_nervio / 2)]
    franjas_x += [(cortes_x[k] + esp_nervio / 2, cortes_x[k + 1] - esp_nervio / 2)
                  for k in range(1, len(cortes_x) - 2)]
    franjas_x += [(cortes_x[-2] + esp_nervio / 2, cortes_x[-1])]
    limite = circulo(r_libre)
    ranuras, descartadas = [], 0
    for (y0, y1) in franjas_y:
        for (x0, x1) in franjas_x:
            celda = recortar([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], limite)
            if not celda:
                continue
            mm = [(x * 1000, y * 1000) for (x, y) in celda]
            if area(mm) < AREA_MIN_MM2:
                descartadas += 1
                continue
            ranuras.append(mm)
    exterior = [(x * 1000, y * 1000) for (x, y) in circulo(radio, 720)]
    return exterior, ranuras, descartadas, radio * 1000, r_in * 1000


def svg(ruta, exterior, ranuras, radio_mm):
    m = 5
    lado = 2 * radio_mm + 2 * m
    def camino(pol):
        return "M " + " L ".join(f"{x + radio_mm + m:.3f},{radio_mm + m - y:.3f}" for x, y in pol) + " Z"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{lado:.2f}mm" height="{lado:.2f}mm" '
                f'viewBox="0 0 {lado:.2f} {lado:.2f}">\n')
        f.write('<g fill="none" stroke="#ff0000" stroke-width="0.1">\n')
        for pol in [exterior] + ranuras:
            f.write(f'<path d="{camino(pol)}"/>\n')
        f.write("</g>\n</svg>\n")


def dxf(ruta, exterior, ranuras):
    """DXF R12 con una POLYLINE cerrada por contorno, en mm."""
    lineas = ["0", "SECTION", "2", "HEADER", "9", "$INSUNITS", "70", "4", "0", "ENDSEC",
              "0", "SECTION", "2", "ENTITIES"]
    for pol in [exterior] + ranuras:
        lineas += ["0", "POLYLINE", "8", "CORTE", "66", "1", "70", "1"]
        for x, y in pol:
            lineas += ["0", "VERTEX", "8", "CORTE", "10", f"{x:.4f}", "20", f"{y:.4f}"]
        lineas += ["0", "SEQEND"]
    lineas += ["0", "ENDSEC", "0", "EOF"]
    with open(ruta, "w", encoding="ascii") as f:
        f.write("\n".join(lineas) + "\n")


def main():
    P = parametros()
    exterior, ranuras, descartadas, radio_mm, r_in_mm = rejilla(P)
    svg(os.path.join(AQUI, "rejilla_banco.svg"), exterior, ranuras, radio_mm)
    dxf(os.path.join(AQUI, "rejilla_banco.dxf"), exterior, ranuras)
    largo_tira = 2 * math.pi * (r_in_mm + ESPESOR_TIRA * 500) + SOLAPE_DUCTO * 1000
    print(f"rejilla: {2 * radio_mm:.1f} mm de diámetro, {len(ranuras)} ranuras "
          f"({descartadas} astillas contra el aro quedan llenas)")
    print(f"ducto: diámetro interior {2 * r_in_mm:.1f} mm, tira de {P['alto'] * 1000:.0f} x "
          f"{largo_tira:.0f} mm en policarbonato de 1 mm, con {SOLAPE_DUCTO * 1000:.0f} mm de solape")


if __name__ == "__main__":
    main()
