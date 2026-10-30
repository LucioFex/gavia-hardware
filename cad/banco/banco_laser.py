"""Gavia, kit del banco de empuje para corte láser en MDF.

Dibuja en 2D todas las piezas del banco de un ducto (base, patas, separadores de la celda,
plataforma, parantes, refuerzos, anillos, listones y placa del motor) para cortarlas en MDF
(fibrofácil) de 5,5 mm. Las medidas del ducto salen de gavia_aro.py a través de rejilla_banco.py,
así que si cambia el aro cambia el banco. No necesita Blender ni librerías.

    python banco_laser.py

Escribe banco_mdf_1 y banco_mdf_2 (.svg y .dxf, dos planchas de 600 x 400 mm), el esquema
banco_armado.svg, y anota la tara del banco, la altura de la hélice y dónde van las ranuras del tubo.
Rojo corta, azul graba el nombre de la pieza (opcional).
"""
import math
import os

from rejilla_banco import AQUI, ESPESOR_TIRA, SOLAPE_DUCTO, area, circulo, parametros, rejilla

E = 5.5  # MDF de 5,5 mm
J = 0.1  # juego de los encastres: la ranura mide E + J
PLANCHA = (600.0, 400.0)
MARGEN = 5.0
AIRE = 200.0  # aire libre debajo de la boca de entrada (la hélice sopla hacia arriba)

# motor Hobbywing XRotor 2812 (tabla del fabricante): cuerpo de 34 x 25,5 mm, 4 x M3 en un círculo de 19 mm
MOTOR_DIAM = 34.0
MOTOR_ALTO = 25.5
CIRCULO_M3 = 19.0
CUADROS_M3 = (16.0, 19.0)  # por si el motor que llega trae 16 x 16 o 19 x 19: colisos en diagonal
M3 = 3.2
EJE = 10.0  # agujero central para el eje y el seguro de abajo
HELICE_SOBRE_BASE = 29.5  # de la base del motor al plano de la hélice (aprox., a validar con el motor)
MEDIO_ESPESOR_HELICE = 5.0  # aprox., a validar

# celda de carga de barra de 80 x 12,7 x 12,7 mm, dos agujeros M4 o M5 por punta (aprox., a validar)
CELDA_LARGO = 80.0
CELDA_LADO = 12.7
COLISO_CELDA = (3.0, 28.0)  # desde cada punta: cubre separaciones de 10 a 20 mm entre agujeros
ANCHO_COLISO = 5.5  # pasa M4 y M5
SEPARADOR = (36.0, 22.0)  # dos capas por punta: 11 mm de aire entre la celda y cada placa
SEPARADOR_DESDE = 8.0  # arranca a 8 mm del centro de la celda y pasa 4 mm su punta

# alturas medidas desde el borde de entrada del tubo
LISTON_Z0 = 8.0  # arriba de la rejilla de entrada, que ocupa de 1 a 7 mm
LISTON_ALTO = 28.0
LISTON_X = 24.0  # los dos listones van a +-24 mm del eje, a los costados del motor
PLACA_Z0 = 14.0  # la placa del motor pasa por una ventana de los listones
PLACA_PROF = 40.0
ANILLO_Z = (40.0, 70.0)
ANILLO_ANCHO = 12.0
TALON = 24.0  # ancho del talón del anillo que entra en el parante
SOBRESALE = 3.0
PARANTE_ANCHO = 80.0
SOBRE_TUBO = 5.0
PLATAFORMA = (300.0, 390.0)
REFUERZO = (60.0, 140.0)
BASE = (420.0, 120.0)
PATA = (120.0, 30.0)

# densidades para la tara (aprox., a validar)
RHO_MDF = 750.0
RHO_ACRILICO = 1190.0
RHO_PC = 1200.0
MASA_MOTOR = 0.0834  # Hobbywing
MASA_OTROS = 0.110  # hélice, ESC y manguera del labio (aprox., a validar)
EMPUJE_TABLA = 2.771  # kg al 100 % con 8 pulgadas en 6S (tabla de Hobbywing)


# ---------------------------------------------------------------- geometría 2D
def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def circ(cx, cy, r, n=48):
    return [(cx + x, cy + y) for x, y in circulo(r, n)]


def coliso(x0, x1, y, ancho, n=12):
    """Ranura con puntas redondas entre los centros (x0, y) y (x1, y)."""
    r = ancho / 2
    pts = [(x1 + r * math.cos(a), y + r * math.sin(a))
           for a in [-math.pi / 2 + math.pi * k / n for k in range(n + 1)]]
    pts += [(x0 + r * math.cos(a), y + r * math.sin(a))
            for a in [math.pi / 2 + math.pi * k / n for k in range(n + 1)]]
    return pts


def girar(pol, ang):
    c, s = math.cos(ang), math.sin(ang)
    return [(x * c - y * s, x * s + y * c) for x, y in pol]


def arco(cx, cy, r, a0, a1, n):
    return [(cx + r * math.cos(a0 + (a1 - a0) * k / n), cy + r * math.sin(a0 + (a1 - a0) * k / n))
            for k in range(n + 1)]


def caja(pols):
    xs = [x for p in pols for x, _ in p]
    ys = [y for p in pols for _, y in p]
    return min(xs), min(ys), max(xs), max(ys)


# ---------------------------------------------------------------- piezas
def piezas(P):
    """Cada pieza: nombre, cantidad, contornos (el primero es el de afuera) y masa por unidad."""
    r_in = P["helice_pulg"] * 25.4 / 2 + P["holgura_punta"] * 1000  # cara interior del tubo
    r_tubo = r_in + ESPESOR_TIRA * 1000
    alto = P["alto"] * 1000
    r_anillo_in = r_tubo + 0.3
    r_anillo = r_anillo_in + ANILLO_ANCHO
    y_parante = r_anillo + 1.1  # cara de adentro del parante
    y_afuera = y_parante + E + SOBRESALE  # punta de los talones y de los listones
    z_tope = AIRE + alto + SOBRE_TUBO
    ranura = E + J
    out = []

    # plataforma: apoya en la punta libre de la celda y lleva todo lo que se pesa
    px, py = PLATAFORMA[0] / 2, PLATAFORMA[1] / 2
    huecos = [coliso(CELDA_LARGO / 2 - COLISO_CELDA[1], CELDA_LARGO / 2 - COLISO_CELDA[0], 0, ANCHO_COLISO)]
    for s in (-1, 1):
        y0, y1 = sorted((s * (y_parante - J / 2), s * (y_parante + E + J / 2)))
        for xc in (-25.0, 25.0):
            huecos.append(rect(xc - 10 - J / 2, y0, xc + 10 + J / 2, y1))
        g0, g1 = sorted((s * (y_parante + E + 10.5), s * (y_parante + E + 50.5)))
        huecos.append(rect(-ranura / 2, g0, ranura / 2, g1))
    out.append(dict(nombre="PLATAFORMA", n=1, cont=[rect(-px, -py, px, py)] + huecos))

    # parante: sostiene los listones y los dos anillos, con la ranura de los talones abierta arriba
    w = PARANTE_ANCHO / 2
    t = TALON / 2 + J / 2
    z_rej = AIRE + ANILLO_Z[0]
    ext = [(-w, 0), (-35, 0), (-35, -E), (-15, -E), (-15, 0), (15, 0), (15, -E), (35, -E), (35, 0), (w, 0),
           (w, z_tope), (t, z_tope), (t, z_rej), (-t, z_rej), (-t, z_tope), (-w, z_tope)]
    huecos = [rect(s * LISTON_X - ranura / 2, AIRE + LISTON_Z0 - J / 2, s * LISTON_X + ranura / 2,
                   AIRE + LISTON_Z0 + LISTON_ALTO + J / 2) for s in (-1, 1)]
    huecos.append(rect(-ranura / 2, 20, ranura / 2, 120))
    out.append(dict(nombre="PARANTE", n=2, cont=[ext] + huecos, texto=(0, 60)))

    # refuerzo: escuadra entre el parante y la plataforma, por afuera
    a, b = REFUERZO
    ext = [(0, 0), (10.5, 0), (10.5, -E), (50.5, -E), (50.5, 0), (a, 0), (0, b), (0, 120), (-E, 120),
           (-E, 20), (0, 20)]
    out.append(dict(nombre="REFUERZO", n=2, cont=[ext], texto=(14, 30)))

    # listón: cruza el ducto a un costado del motor, de parante a parante
    ext = rect(-y_afuera, 0, y_afuera, LISTON_ALTO)
    hueco = rect(-PLACA_PROF / 2 - J / 2, PLACA_Z0 - LISTON_Z0, PLACA_PROF / 2 + J / 2,
                 PLACA_Z0 - LISTON_Z0 + E + J)
    out.append(dict(nombre="LISTON", n=2, cont=[ext, hueco], texto=(-90, 8)))

    # anillo: abraza el tubo, con dos talones que bajan por la ranura de los parantes
    y_t = math.sqrt(r_anillo ** 2 - (TALON / 2) ** 2)
    a_t = math.atan2(y_t, TALON / 2)
    ext = arco(0, 0, r_anillo, -a_t, a_t, 120)
    ext += [(TALON / 2, y_afuera), (-TALON / 2, y_afuera)]
    ext += arco(0, 0, r_anillo, math.pi - a_t, math.pi + a_t, 120)
    ext += [(-TALON / 2, -y_afuera), (TALON / 2, -y_afuera)]
    out.append(dict(nombre="ANILLO", n=2, cont=[ext, circ(0, 0, r_anillo_in, 360)],
                    texto=(0, -(r_anillo_in + r_anillo) / 2 - 2)))

    # placa del motor: pasa por la ventana de los dos listones
    xp = LISTON_X + E / 2 + SOBRESALE
    huecos = [circ(0, 0, EJE / 2)]
    huecos += [circ(CIRCULO_M3 / 2 * math.cos(k * math.pi / 2), CIRCULO_M3 / 2 * math.sin(k * math.pi / 2), M3 / 2, 24)
               for k in range(4)]
    r0, r1 = CUADROS_M3[0] / math.sqrt(2), CUADROS_M3[1] / math.sqrt(2)
    huecos += [girar(coliso(r0, r1, 0, M3), math.pi / 4 + k * math.pi / 2) for k in range(4)]
    out.append(dict(nombre="PLACA MOTOR", n=1, cont=[rect(-xp, -PLACA_PROF / 2, xp, PLACA_PROF / 2)] + huecos))

    # base, patas y separadores de la celda
    bx, by = BASE[0] / 2, BASE[1] / 2
    out.append(dict(nombre="BASE", n=1, cont=[rect(-bx, -by, bx, by), coliso(
        -CELDA_LARGO / 2 + COLISO_CELDA[0], -CELDA_LARGO / 2 + COLISO_CELDA[1], 0, ANCHO_COLISO)],
        texto=(110, -4)))
    out.append(dict(nombre="PATA", n=4, cont=[rect(0, 0, PATA[0], PATA[1])], texto=(60, 12)))
    sx, sy = SEPARADOR
    d = SEPARADOR_DESDE  # el separador cubre la punta de la celda, con el mismo coliso que las placas
    out.append(dict(nombre="SEPARADOR", n=4, cont=[rect(0, 0, sx, sy), coliso(
        CELDA_LARGO / 2 - COLISO_CELDA[1] - d, CELDA_LARGO / 2 - COLISO_CELDA[0] - d, sy / 2, ANCHO_COLISO)],
        texto=None))
    for p in out:
        afuera = area(p["cont"][0])
        p["area"] = afuera - sum(area(h) for h in p["cont"][1:])
        p["masa"] = p["area"] * E * 1e-9 * RHO_MDF
    geo = dict(r_in=r_in, r_tubo=r_tubo, r_anillo=r_anillo, r_anillo_in=r_anillo_in, y_parante=y_parante,
               y_afuera=y_afuera, alto=alto, z_tope=z_tope)
    return {p["nombre"]: p for p in out}, geo


# ---------------------------------------------------------------- anidado en dos planchas
def ubicar(pieza, x, y, rot=0.0):
    """Gira la pieza y la apoya con su esquina de abajo a la izquierda en (x, y)."""
    cont = [girar(c, rot) for c in pieza["cont"]]
    x0, y0, _, _ = caja(cont)
    cont = [[(px - x0 + x, py - y0 + y) for px, py in c] for c in cont]
    texto = None
    if pieza.get("texto", 0) is not None:
        tx, ty = pieza.get("texto") or (0, 0)
        tx, ty = girar([(tx, ty)], rot)[0]
        texto = (tx - x0 + x, ty - y0 + y, pieza["nombre"], math.degrees(rot))
    return dict(nombre=pieza["nombre"], cont=cont, texto=texto)


def centrar_en(pieza, cx, cy, rot=0.0):
    x0, y0, x1, y1 = caja([girar(c, rot) for c in pieza["cont"]])
    return ubicar(pieza, cx - (x1 - x0) / 2, cy - (y1 - y0) / 2, rot)


def planchas(Z):
    m = MARGEN
    h = math.pi / 2
    p1 = [ubicar(Z["PLATAFORMA"], m, m)]
    x = m + PLATAFORMA[0] + m
    for _ in range(2):
        p1.append(ubicar(Z["PARANTE"], x, m))
        x += PARANTE_ANCHO + m
    for _ in range(2):
        p1.append(ubicar(Z["LISTON"], x, m, h))
        x += LISTON_ALTO + m

    p2 = []
    anillo = caja([girar(c, h) for c in Z["ANILLO"]["cont"]])
    ancho_anillo, alto_anillo = anillo[2] - anillo[0], anillo[3] - anillo[1]
    centros = [(m + ancho_anillo / 2, m + alto_anillo / 2), (2 * m + 1.5 * ancho_anillo, m + alto_anillo / 2)]
    for cx, cy in centros:
        p2.append(centrar_en(Z["ANILLO"], cx, cy, h))
    # adentro del primer anillo: las cuatro patas
    cx, cy = centros[0]
    for k in range(4):
        p2.append(centrar_en(Z["PATA"], cx, cy + (k - 1.5) * (PATA[1] + 3)))
    # adentro del segundo: la placa del motor y los cuatro separadores
    cx, cy = centros[1]
    p2.append(centrar_en(Z["PLACA MOTOR"], cx, cy + 32))
    for k in range(4):
        p2.append(centrar_en(Z["SEPARADOR"], cx + (k % 2 - 0.5) * (SEPARADOR[0] + 4),
                             cy - 18 - (k // 2) * (SEPARADOR[1] + 4)))
    y = m + alto_anillo + m
    p2.append(ubicar(Z["BASE"], m, y))
    x = m + BASE[0] + m
    for k in range(2):
        p2.append(ubicar(Z["REFUERZO"], x, y + k * (REFUERZO[0] + E + m), h))
    return [p1, p2], centros, ancho_anillo


def revisar(plancha, nombre, centros_anillos=None, r_hueco=None):
    """Que nada se salga de la plancha ni se pise (por cajas, salvo lo que va adentro de un anillo)."""
    avisos = []
    cajas = []
    for p in plancha:
        x0, y0, x1, y1 = caja(p["cont"])
        if x0 < 0 or y0 < 0 or x1 > PLANCHA[0] or y1 > PLANCHA[1]:
            avisos.append(f"{nombre}: {p['nombre']} se sale de la plancha")
        adentro = False
        if centros_anillos and p["nombre"] != "ANILLO":
            for cx, cy in centros_anillos:
                esquinas = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
                if all(math.hypot(ex - cx, ey - cy) < r_hueco - 3 for ex, ey in esquinas):
                    adentro = True
        if not adentro:
            cajas.append((p["nombre"], x0, y0, x1, y1))
    for i in range(len(cajas)):
        for j in range(i + 1, len(cajas)):
            a, b = cajas[i], cajas[j]
            if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                avisos.append(f"{nombre}: {a[0]} pisa a {b[0]}")
    return avisos


# ---------------------------------------------------------------- salida
def svg(ruta, plancha):
    W, H = PLANCHA
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}mm" height="{H:.0f}mm" '
                f'viewBox="0 0 {W:.0f} {H:.0f}">\n')
        f.write('<g fill="none" stroke="#ff0000" stroke-width="0.1">\n')
        for p in plancha:
            for c in p["cont"]:
                f.write('<path d="M ' + " L ".join(f"{x:.3f},{H - y:.3f}" for x, y in c) + ' Z"/>\n')
        f.write('</g>\n<g fill="#0000ff" font-family="Arial, sans-serif" font-size="5" text-anchor="middle">\n')
        for p in plancha:
            if p["texto"]:
                x, y, txt, rot = p["texto"]
                f.write(f'<text x="{x:.2f}" y="{H - y:.2f}" transform="rotate({-rot:.0f} {x:.2f} {H - y:.2f})">'
                        f'{txt}</text>\n')
        f.write("</g>\n</svg>\n")


def dxf(ruta, plancha):
    """DXF R12: contornos en la capa CORTE y nombres en la capa GRABADO, en mm."""
    lineas = ["0", "SECTION", "2", "HEADER", "9", "$INSUNITS", "70", "4", "0", "ENDSEC",
              "0", "SECTION", "2", "ENTITIES"]
    for p in plancha:
        for c in p["cont"]:
            lineas += ["0", "POLYLINE", "8", "CORTE", "62", "1", "66", "1", "70", "1"]
            for x, y in c:
                lineas += ["0", "VERTEX", "8", "CORTE", "10", f"{x:.4f}", "20", f"{y:.4f}"]
            lineas += ["0", "SEQEND"]
        if p["texto"]:
            x, y, txt, rot = p["texto"]
            lineas += ["0", "TEXT", "8", "GRABADO", "62", "5", "10", f"{x:.3f}", "20", f"{y:.3f}", "40", "5",
                       "1", txt, "50", f"{rot:.0f}", "72", "1", "11", f"{x:.3f}", "21", f"{y:.3f}"]
    lineas += ["0", "ENDSEC", "0", "EOF"]
    with open(ruta, "w", encoding="ascii") as f:
        f.write("\n".join(lineas) + "\n")


def esquema(ruta, P, geo, rejilla_info):
    """Vista de frente, cortada por el centro: el banco armado con cada pieza rotulada."""
    C, CR, SEC, ESP, LIN, NAR = "#1F1F1F", "#F8F4EB", "#5C534A", "#EAE1CF", "#D9CFC0", "#F26B1D"
    alto, r_in, r_tubo = geo["alto"], geo["r_in"], geo["r_tubo"]
    # alturas desde la mesa
    z_base = 2 * E
    z_celda = z_base + E + 2 * E
    z_plat = z_celda + CELDA_LADO + 2 * E
    z0 = z_plat + E  # cara de arriba de la plataforma
    zt = z0 + AIRE  # boca de entrada del tubo
    zh = zt + PLACA_Z0 + E + HELICE_SOBRE_BASE
    X0, X1, Y1 = -420.0, 420.0, zt + alto + 40
    fy = lambda z: Y1 - z  # noqa: E731
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{X0:.0f} 0 {X1 - X0:.0f} {Y1 + 30:.0f}" '
         f'font-family="WS, Work Sans, sans-serif">']

    def r(x0, z0_, x1, z1, fill, stroke=C, sw=0.6, extra=""):
        o.append(f'<rect x="{min(x0, x1):.2f}" y="{fy(max(z0_, z1)):.2f}" width="{abs(x1 - x0):.2f}" '
                 f'height="{abs(z1 - z0_):.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>')

    # mesa
    o.append(f'<line x1="-300" y1="{fy(0):.2f}" x2="300" y2="{fy(0):.2f}" stroke="{C}" stroke-width="1.2"/>')
    o.append(f'<rect x="-300" y="{fy(0):.2f}" width="600" height="14" fill="{LIN}"/>')
    # parante, de fondo
    w, t = PARANTE_ANCHO / 2, TALON / 2
    zt_rej = z0 + AIRE + ANILLO_Z[0]
    zt_top = z0 + geo["z_tope"]
    o.append(f'<path d="M {-w} {fy(z0):.2f} L {w} {fy(z0):.2f} L {w} {fy(zt_top):.2f} L {t} {fy(zt_top):.2f} '
             f'L {t} {fy(zt_rej):.2f} L {-t} {fy(zt_rej):.2f} L {-t} {fy(zt_top):.2f} L {-w} {fy(zt_top):.2f} Z" '
             f'fill="{ESP}" fill-opacity="0.55" stroke="{SEC}" stroke-width="0.5" stroke-dasharray="3 2"/>')
    # patas, base, separadores, celda y plataforma
    for s in (-1, 1):
        r(s * BASE[0] / 2, 0, s * (BASE[0] / 2 - PATA[1]), z_base, ESP)
    r(-BASE[0] / 2, z_base, BASE[0] / 2, z_base + E, ESP)
    r(-CELDA_LARGO / 2 - 4, z_base + E, -SEPARADOR_DESDE, z_celda, ESP)
    r(-CELDA_LARGO / 2, z_celda, CELDA_LARGO / 2, z_celda + CELDA_LADO, "#B9B4AC", sw=0.6)
    r(SEPARADOR_DESDE, z_celda + CELDA_LADO, CELDA_LARGO / 2 + 4, z_plat, ESP)
    r(-PLATAFORMA[0] / 2, z_plat, PLATAFORMA[0] / 2, z0, ESP)
    # sargentos en las puntas de la base
    for s in (-1, 1):
        xc = s * (BASE[0] / 2 - 15)
        o.append(f'<path d="M {xc - 9:.1f} {fy(z_base + E + 9):.2f} L {xc + 9:.1f} {fy(z_base + E + 9):.2f} '
                 f'M {xc:.1f} {fy(z_base + E + 9):.2f} L {xc:.1f} {fy(z_base + E):.2f}" stroke="{C}" '
                 f'stroke-width="2.2" stroke-linecap="round" fill="none"/>')
    # tubo de policarbonato y anillos
    for s in (-1, 1):
        r(s * r_in, zt, s * r_tubo, zt + alto, CR, stroke=SEC, sw=0.5)
        for za in ANILLO_Z:
            r(s * (geo["r_anillo_in"]), zt + za, s * geo["r_anillo"], zt + za + E, ESP)
        # labio: manguera abierta calzada en el borde de entrada
        xc = s * (r_in + r_tubo) / 2
        o.append(f'<path d="M {xc - 6:.2f} {fy(zt + 4):.2f} A 9 9 0 1 0 {xc + 6:.2f} {fy(zt + 4):.2f}" '
                 f'fill="none" stroke="{C}" stroke-width="2.4"/>')
    # rejillas en las dos bocas, flejes de 2 mm cada 7
    paso = (P["abertura_rejilla"] + P["fleje_espesor"]) * 1000
    fl, prof = P["fleje_espesor"] * 1000, P["fleje_prof"] * 1000
    n = int(rejilla_info / paso)
    for zr in (zt + 1, zt + alto - 1 - prof):
        for k in range(-n, n + 1):
            x = k * paso
            if abs(x) + fl / 2 < rejilla_info:
                r(x - fl / 2, zr, x + fl / 2, zr + prof, NAR, stroke="none", sw=0)
        borde = zr if zr < zt + 10 else zr + prof - 1  # el aro de la rejilla, del lado de afuera
        r(-rejilla_info, borde, rejilla_info, borde + 1, NAR, stroke="none", sw=0)
    # listones cortados, placa, motor y hélice
    for s in (-1, 1):
        r(s * (LISTON_X - E / 2), zt + LISTON_Z0, s * (LISTON_X + E / 2), zt + LISTON_Z0 + LISTON_ALTO, ESP)
    xp = LISTON_X + E / 2 + SOBRESALE
    r(-xp, zt + PLACA_Z0, xp, zt + PLACA_Z0 + E, ESP)
    r(-MOTOR_DIAM / 2, zt + PLACA_Z0 + E, MOTOR_DIAM / 2, zt + PLACA_Z0 + E + MOTOR_ALTO, C, stroke=C)
    r_hel = P["helice_pulg"] * 25.4 / 2
    o.append(f'<line x1="{-r_hel:.1f}" y1="{fy(zh):.2f}" x2="{r_hel:.1f}" y2="{fy(zh):.2f}" stroke="{SEC}" '
             f'stroke-width="2.6" stroke-linecap="round"/>')
    o.append(f'<circle cx="0" cy="{fy(zh):.2f}" r="5" fill="{C}"/>')
    # aire
    for s in (-1, 1):
        o.append(f'<path d="M {s * 175} {fy(zt - 60):.2f} Q {s * 60} {fy(zt - 55):.2f} {s * 55} {fy(zt - 12):.2f}" '
                 f'fill="none" stroke="{SEC}" stroke-width="0.8" stroke-dasharray="4 3" marker-end="url(#f)"/>')
    o.append(f'<path d="M 0 {fy(zt + alto + 6):.2f} L 0 {fy(zt + alto + 32):.2f}" stroke="{SEC}" '
             f'stroke-width="0.8" stroke-dasharray="4 3" marker-end="url(#f)"/>')
    o.insert(1, f'<defs><marker id="f" viewBox="0 0 6 6" refX="3" refY="3" markerWidth="5" markerHeight="5" '
                f'orient="auto"><path d="M0 0 L6 3 L0 6 Z" fill="{SEC}"/></marker></defs>')
    # cota del aire libre
    xa = -135
    o.append(f'<g stroke="{SEC}" stroke-width="0.5"><line x1="{xa}" y1="{fy(z0):.2f}" x2="{xa}" y2="{fy(zt):.2f}"/>'
             f'<line x1="{xa - 4}" y1="{fy(z0):.2f}" x2="{xa + 4}" y2="{fy(z0):.2f}"/>'
             f'<line x1="{xa - 4}" y1="{fy(zt):.2f}" x2="{xa + 4}" y2="{fy(zt):.2f}"/></g>')
    o.append(f'<text x="{xa - 6}" y="{fy((z0 + zt) / 2):.2f}" font-size="9" fill="{SEC}" text-anchor="end">'
             f'{AIRE:.0f} mm de aire libre</text>')
    # rótulos: (x del punto, z del punto, lado, z del texto, texto)
    rot = [
        (rejilla_info - 20, zt + alto - 4, 1, zt + alto + 14, "Rejilla de salida, acrílico"),
        (r_hel - 30, zh, 1, zt + 70, "Hélice de 8 pulgadas"),
        (MOTOR_DIAM / 2, zt + PLACA_Z0 + E + 14, 1, zt + 50, "Motor"),
        (LISTON_X + E / 2, zt + LISTON_Z0 + 3, 1, zt + 30, "Listón y placa del motor"),
        (w, z0 + 120, 1, z0 + 120, "Parante, detrás del tubo"),
        (PLATAFORMA[0] / 2 - 10, z0 - E / 2, 1, z0 + 22, "Plataforma: todo lo de arriba se pesa"),
        (CELDA_LARGO / 2 - 4, z_celda + CELDA_LADO / 2, 1, z_celda - 6, "Celda de carga y separadores"),
        (r_tubo, zt + alto - 20, -1, zt + alto + 14, "Tubo de policarbonato de 1 mm"),
        (geo["r_anillo"], zt + ANILLO_Z[1] + 3, -1, zt + 70, "Anillo"),
        ((r_in + r_tubo) / 2 + 8, zt + 2, -1, zt - 10, "Rejilla de entrada y labio de manguera"),
        (BASE[0] / 2 - 15, z_base + E + 9, -1, z_base + 44, "Sargento a la mesa"),
        (BASE[0] / 2 - 30, z_base + E / 2, -1, z_base + 8, "Base y patas"),
    ]
    xt = {1: 235.0, -1: -235.0}
    for x, z, lado, ztx, txt in rot:
        x = lado * abs(x)
        o.append(f'<path d="M {x:.1f} {fy(z):.2f} L {xt[lado] - lado * 8:.1f} {fy(ztx):.2f} L {xt[lado] - lado * 3:.1f} '
                 f'{fy(ztx):.2f}" fill="none" stroke="{SEC}" stroke-width="0.4"/>')
        anc = "start" if lado > 0 else "end"
        o.append(f'<text x="{xt[lado]:.1f}" y="{fy(ztx) + 3:.2f}" font-size="9" fill="{C}" text-anchor="{anc}">'
                 f'{txt}</text>')
    o.append("</svg>")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(o) + "\n")


def ranuras_tubo(geo):
    """Dónde cortar las cuatro ranuras abiertas del borde de entrada, medido sobre la tira desde la punta
    que queda adentro del solape (esa punta va a 0 grados, lejos de los listones)."""
    r_med = geo["r_in"] + ESPESOR_TIRA * 500
    res = []
    for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        bordes = []
        for x in (sx * (LISTON_X - E / 2 - 0.3), sx * (LISTON_X + E / 2 + 0.3)):
            ang = math.atan2(sy * math.sqrt(r_med ** 2 - x ** 2), x) % (2 * math.pi)
            bordes.append(ang * r_med)
        res.append((min(bordes), max(bordes)))
    return sorted(res), r_med


def main():
    P = parametros()
    Z, geo = piezas(P)
    hojas, centros, ancho_anillo = planchas(Z)
    avisos = revisar(hojas[0], "plancha 1")
    avisos += revisar(hojas[1], "plancha 2", centros, geo["r_anillo_in"])
    for i, hoja in enumerate(hojas, 1):
        svg(os.path.join(AQUI, f"banco_mdf_{i}.svg"), hoja)
        dxf(os.path.join(AQUI, f"banco_mdf_{i}.dxf"), hoja)
    ext, ranuras, _, radio_rej, _ = rejilla(P)
    esquema(os.path.join(AQUI, "banco_armado.svg"), P, geo, radio_rej)

    # tara: lo que queda sobre la celda
    mdf = sum(Z[k]["masa"] * Z[k]["n"] for k in ("PLATAFORMA", "PARANTE", "REFUERZO", "LISTON", "ANILLO",
                                                 "PLACA MOTOR")) + Z["SEPARADOR"]["masa"] * 2
    rej = 2 * (area(ext) - sum(area(r) for r in ranuras)) * P["fleje_prof"] * 1000 * 1e-9 * RHO_ACRILICO
    tubo = P["alto"] * (2 * math.pi * geo["r_in"] / 1000 + SOLAPE_DUCTO) * ESPESOR_TIRA * RHO_PC
    tara = mdf + rej + tubo + MASA_MOTOR + MASA_OTROS
    pico = tara + EMPUJE_TABLA * 1.25  # con algo de ganancia del ducto (aprox., a validar)
    zh = PLACA_Z0 + E + HELICE_SOBRE_BASE
    alto = geo["alto"]
    print(f"piezas en dos planchas de {PLANCHA[0]:.0f} x {PLANCHA[1]:.0f} mm de MDF de {E} mm")
    for k, p in Z.items():
        print(f"  {k}: {p['n']}")
    print(f"tubo: interior {2 * geo['r_in']:.1f} mm, exterior {2 * geo['r_tubo']:.1f} mm, anillos de "
          f"{2 * geo['r_anillo_in']:.1f} a {2 * geo['r_anillo']:.1f} mm, parantes a {geo['y_parante']:.1f} mm del eje")
    print(f"hélice a {zh:.1f} mm del borde de entrada ({zh - alto / 2:+.1f} mm del centro del tubo, aprox.)")
    print(f"motor a {LISTON_X - E / 2 - MOTOR_DIAM / 2:.2f} mm de cada listón, listones a "
          f"{zh - MEDIO_ESPESOR_HELICE - LISTON_Z0 - LISTON_ALTO:.1f} mm de la hélice (aprox.)")
    print(f"tara sobre la celda: {tara:.2f} kg (MDF {mdf:.2f}, rejillas {rej:.2f}, tubo {tubo:.3f}), "
          f"pico con empuje: {pico:.2f} kg (aprox., a validar)")
    tramos, r_med = ranuras_tubo(geo)
    print(f"ranuras del tubo, abiertas desde el borde de entrada hasta {LISTON_Z0 + LISTON_ALTO + 0.5:.1f} mm "
          f"(desde la punta de adentro de la tira, radio medio {r_med:.1f} mm):")
    for a, b in tramos:
        print(f"  de {a:.0f} a {b:.0f} mm")
    for a in avisos:
        print("AVISO:", a)


if __name__ == "__main__":
    main()
