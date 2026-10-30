"""Gavia, capas del cuerpo del aro para hilo caliente o router CNC.

Dibuja en 2D las tres capas de EPS de 30 mm que, pegadas, forman el cuerpo de 90 mm del aro: los
cuatro agujeros de ducto para el liner de policarbonato de 1 mm, los huecos de mano y el canal del
cuadrado de carbono en la capa del medio, y dos ventanas enfrentadas para cajas estancas
comerciales con la tapa enrasada arriba. Los parámetros se leen de ../blender/gavia_aro.py, así que
si cambian allá cambian acá. No necesita Blender ni librerías.

    python cuerpo_capas.py

Escribe capa_exterior (o capa_arriba y capa_abajo si salen distintas), capa_media y tapon_caja en
SVG y DXF, en mm, el esquema cuerpo_armado.svg, y anota paredes mínimas, choques, volumen y masa.
"""
import ast
import math
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
SCRIPT_ARO = os.path.join(AQUI, "..", "blender", "gavia_aro.py")

CAPA = 30.0  # EPS de 30 mm, tres capas
RHO_EPS = 30.0  # kg/m3
LINER = 1.0  # policarbonato de 1 mm, como el ducto del banco
CANAL = 13.5  # caño de aluminio de 12,7 mm (prototipo) o tubo de carbono de 13 mm, con juego
HUECO_ALTO = 30.0  # los huecos de mano ocupan la capa del medio entera
RADIO_FONDO_HUECO = 9.0  # esquinas redondeadas del fondo del hueco de mano

# caja de paso estanca IP65 Kalop (Unika) de 120 x 170 x 75 mm, MercadoLibre MLAU3893576153
# (medidas del vendedor, a validar con la caja en mano)
CAJA = dict(ancho=120.0, largo=170.0, alto=75.0)
JUEGO_CAJA = 1.0  # por lado
ANGULOS_CAJAS = (0.0, 180.0)  # entre los ductos, donde el modelo pone la batería y la caja de señal
PARED_MIN = 8.0  # pared mínima de espuma que se acepta sin avisar


def parametros():
    """Lee el diccionario de P.update({...}) de gavia_aro.py sin ejecutar Blender."""
    arbol = ast.parse(open(SCRIPT_ARO, encoding="utf-8").read())
    for nodo in ast.walk(arbol):
        if (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Attribute)
                and nodo.func.attr == "update"):
            return ast.literal_eval(nodo.args[0])
    raise RuntimeError("no encontré P.update en gavia_aro.py")


def area(pol):
    return abs(sum(pol[i][0] * pol[(i + 1) % len(pol)][1] - pol[(i + 1) % len(pol)][0] * pol[i][1]
                   for i in range(len(pol)))) / 2


def circ(cx, cy, r, n=360):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def arco(cx, cy, r, a0, a1, n):
    return [(cx + r * math.cos(a0 + (a1 - a0) * k / n), cy + r * math.sin(a0 + (a1 - a0) * k / n))
            for k in range(n + 1)]


def local(ang, u, v):
    """Del marco del radio (u hacia afuera, v tangencial) a x, y."""
    c, s = math.cos(ang), math.sin(ang)
    return (u * c - v * s, u * s + v * c)


# ---------------------------------------------------------------- geometría
def medidas(P):
    mm = 1000.0
    r_hel = P["helice_pulg"] * 25.4 / 2
    r_ducto_modelo = r_hel + P["holgura_punta"] * mm + P["liner"] * mm
    r_mid = P["radio_medio"] * mm
    g = dict(
        r_mid=r_mid,
        r_int=r_mid - r_ducto_modelo - P["pared_ducto"] * mm,
        r_ext=r_mid + r_ducto_modelo + P["pared_ducto"] * mm,
        r_agujero=r_hel + P["holgura_punta"] * mm + LINER,
        hueco_largo=P["hueco_largo"] * mm,
        hueco_prof=P["hueco_prof"] * mm,
        alto=P["alto"] * mm,
    )
    g["centros"] = [(r_mid * math.cos(math.pi / 4 + k * math.pi / 2), r_mid * math.sin(math.pi / 4 + k * math.pi / 2))
                    for k in range(4)]
    g["canal_dist"] = r_mid * math.cos(math.pi / 4)  # distancia del centro a cada lado del cuadrado
    return g


def canal_contornos(g, n_arco=96):
    """Contornos del cuadrado de carbono unido a los cuatro agujeros de ducto.

    El canal y los ductos forman un anillo cerrado: su borde de afuera y su borde de adentro son
    dos contornos. La espuma de la capa del medio queda en dos piezas, una de cada lado."""
    w = CANAL / 2
    R = g["r_agujero"]
    s = math.sqrt(R ** 2 - w ** 2)
    c = g["centros"]
    L = math.dist(c[0], c[1])
    afuera, adentro = [], []
    for k in range(4):
        a, b, sig = c[k], c[(k + 1) % 4], c[(k + 2) % 4]
        d = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        n = (d[1], -d[0])  # normal hacia afuera
        d2 = ((sig[0] - b[0]) / L, (sig[1] - b[1]) / L)
        n2 = (d2[1], -d2[0])
        for signo, cont in ((1, afuera), (-1, adentro)):
            p0 = (a[0] + signo * n[0] * w + d[0] * s, a[1] + signo * n[1] * w + d[1] * s)
            p1 = (a[0] + signo * n[0] * w + d[0] * (L - s), a[1] + signo * n[1] * w + d[1] * (L - s))
            q = (b[0] + signo * n2[0] * w + d2[0] * s, b[1] + signo * n2[1] * w + d2[1] * s)
            a0 = math.atan2(p1[1] - b[1], p1[0] - b[0])
            a1 = math.atan2(q[1] - b[1], q[0] - b[0])
            if signo > 0:  # por afuera del ducto, girando antihorario
                while a1 <= a0:
                    a1 += 2 * math.pi
            else:  # por adentro, el arco corto hacia el centro del aro
                while a1 >= a0:
                    a1 -= 2 * math.pi
            cont += [p0] + arco(b[0], b[1], R, a0, a1, n_arco)
    return afuera, adentro


def borde_interior(g, con_huecos, n_arco=90):
    """Canto interior del aro, con los cuatro huecos de mano si la capa los lleva."""
    r = g["r_int"]
    if not con_huecos:
        return circ(0, 0, r)
    v = g["hueco_largo"] / 2
    u1 = r + g["hueco_prof"]
    rf = RADIO_FONDO_HUECO
    dlt = math.asin(v / r)
    pts = []
    for j in range(4):
        b = j * math.pi / 2
        u0 = math.sqrt(r ** 2 - v ** 2) - 1.0  # arranca adentro del canto, así el corte es limpio
        hueco = [(u0, -v), (u1 - rf, -v)]
        hueco += [(u1 - rf + rf * math.cos(t), -v + rf + rf * math.sin(t))
                  for t in [-math.pi / 2 + (math.pi / 2) * i / 8 for i in range(1, 9)]]
        hueco += [(u1 - rf + rf * math.cos(t), v - rf + rf * math.sin(t))
                  for t in [(math.pi / 2) * i / 8 for i in range(0, 9)]]
        hueco += [(u1 - rf, v), (u0, v)]
        pts += [local(b, uu, vv) for uu, vv in hueco]
        pts += arco(0, 0, r, b + dlt, b + math.pi / 2 - dlt, n_arco)[1:-1]
    return pts


def ventana(g, ang_deg, r0):
    a = math.radians(ang_deg)
    l, w = CAJA["largo"] + 2 * JUEGO_CAJA, CAJA["ancho"] + 2 * JUEGO_CAJA
    return [local(a, r0, -w / 2), local(a, r0 + l, -w / 2), local(a, r0 + l, w / 2), local(a, r0, w / 2)]


def ubicar_ventana(g):
    """Corre la ventana sobre el radio hasta que la pared contra el canal y contra el canto de afuera
    queden parejas."""
    borde_canal = g["canal_dist"] + CANAL / 2
    l, w = CAJA["largo"] + 2 * JUEGO_CAJA, CAJA["ancho"] + 2 * JUEGO_CAJA
    lo, hi = borde_canal, g["r_ext"]
    for _ in range(60):
        r0 = (lo + hi) / 2
        p_canal = r0 - borde_canal
        p_canto = g["r_ext"] - math.hypot(r0 + l, w / 2)
        lo, hi = (r0, hi) if p_canal < p_canto else (lo, r0)
    return r0, p_canal, p_canto


def dist_seg(p, a, b):
    ax, ay, bx, by = a[0], a[1], b[0], b[1]
    t = max(0.0, min(1.0, ((p[0] - ax) * (bx - ax) + (p[1] - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2)))
    return math.hypot(p[0] - ax - t * (bx - ax), p[1] - ay - t * (by - ay))


def capas(g):
    r0, p_canal, p_canto = ubicar_ventana(g)
    ventanas = [ventana(g, a, r0) for a in ANGULOS_CAJAS]
    dos = 2 * CAPA
    en_abajo = CAJA["alto"] > dos  # si la caja pasa de 60 mm, la ventana baja a la capa de abajo
    ductos = [circ(cx, cy, g["r_agujero"]) for cx, cy in g["centros"]]
    afuera, adentro = canal_contornos(g)
    exterior = circ(0, 0, g["r_ext"], 720)
    arriba = [exterior, borde_interior(g, False)] + ductos + ventanas
    media = [exterior, afuera, adentro, borde_interior(g, True)] + ventanas
    abajo = [exterior, borde_interior(g, False)] + ductos + (ventanas if en_abajo else [])
    l, w = CAJA["largo"] + 2 * JUEGO_CAJA, CAJA["ancho"] + 2 * JUEGO_CAJA
    tapon_alto = 3 * CAPA - CAJA["alto"] if en_abajo else 0.0
    tapon = [[(0, 0), (l, 0), (l, w), (0, w)]]
    info = dict(r0=r0, p_canal=p_canal, p_canto=p_canto, en_abajo=en_abajo, tapon_alto=tapon_alto)
    return dict(arriba=arriba, media=media, abajo=abajo, tapon=tapon, ventanas=ventanas,
                afuera=afuera, adentro=adentro), info


def revisar(g, C, info):
    """Paredes mínimas entre lo que se corta, en mm."""
    r = []
    r_ag = g["r_agujero"]
    r.append(("ducto contra canto interior", g["r_mid"] - r_ag - g["r_int"]))
    r.append(("ducto contra canto exterior", g["r_ext"] - g["r_mid"] - r_ag))
    r.append(("hueco de mano contra canal de carbono", g["canal_dist"] - CANAL / 2 - g["r_int"] - g["hueco_prof"]))
    esq = local(0, g["r_int"] + g["hueco_prof"], g["hueco_largo"] / 2)
    r.append(("hueco de mano contra ducto", min(math.dist(esq, c) for c in g["centros"]) - r_ag))
    r.append(("ventana contra canal de carbono", info["p_canal"]))
    r.append(("ventana contra canto exterior", info["p_canto"]))
    peor = 1e9
    for v in C["ventanas"]:
        for c in g["centros"]:
            d = min(dist_seg(c, v[i], v[(i + 1) % 4]) for i in range(4))
            peor = min(peor, d - r_ag)
    r.append(("ventana contra ducto", peor))
    return r


# ---------------------------------------------------------------- salida
def svg(ruta, contornos, lado):
    m = 5
    W = lado + 2 * m
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.1f}mm" height="{W:.1f}mm" '
                f'viewBox="0 0 {W:.1f} {W:.1f}">\n<g fill="none" stroke="#ff0000" stroke-width="0.2">\n')
        for c in contornos:
            f.write('<path d="M ' + " L ".join(f"{x + W / 2:.3f},{W / 2 - y:.3f}" for x, y in c) + ' Z"/>\n')
        f.write("</g>\n</svg>\n")


def dxf(ruta, contornos):
    lineas = ["0", "SECTION", "2", "HEADER", "9", "$INSUNITS", "70", "4", "0", "ENDSEC",
              "0", "SECTION", "2", "ENTITIES"]
    for c in contornos:
        lineas += ["0", "POLYLINE", "8", "CORTE", "66", "1", "70", "1"]
        for x, y in c:
            lineas += ["0", "VERTEX", "8", "CORTE", "10", f"{x:.4f}", "20", f"{y:.4f}"]
        lineas += ["0", "SEQEND"]
    lineas += ["0", "ENDSEC", "0", "EOF"]
    with open(ruta, "w", encoding="ascii") as f:
        f.write("\n".join(lineas) + "\n")


def esquema(ruta, g, C):
    """Las tres capas en explosión, vistas desde arriba y de costado."""
    C1, SEC, ESP, LADO = "#1F1F1F", "#5C534A", "#EAE1CF", "#D3C7B2"
    giro, k = math.radians(-28), 0.42
    sep = 250.0  # separación de la explosión, en mm de pantalla
    cg, sg = math.cos(giro), math.sin(giro)

    def proy(x, y, z):
        xr, yr = x * cg - y * sg, x * sg + y * cg
        return xr, -yr * k - z

    def camino(conts, z):
        d = ""
        for c in conts:
            pts = [proy(x, y, z) for x, y in c[::max(1, len(c) // 240)]]
            d += "M " + " L ".join(f"{px:.1f},{py:.1f}" for px, py in pts) + " Z "
        return d

    niveles = [("abajo", 0.0), ("media", sep + CAPA), ("arriba", 2 * (sep + CAPA))]
    o = []
    for nombre, z in niveles:
        conts = C[nombre]
        o.append(f'<path d="{camino(conts, z)}" fill="{LADO}" fill-rule="evenodd" stroke="{C1}" '
                 f'stroke-width="0.7"/>')
        o.append(f'<path d="{camino(conts, z + CAPA)}" fill="{ESP}" fill-rule="evenodd" stroke="{C1}" '
                 f'stroke-width="0.9"/>')

    def borde_derecho(z):
        pts = [proy(x, y, z + CAPA) for x, y in C["arriba"][0]]
        return max(pts, key=lambda p: p[0])

    za, zm, zt = (z for _, z in niveles)
    va = C["ventanas"][0]
    centro_v = (sum(p[0] for p in va) / 4, sum(p[1] for p in va) / 4)
    lado_canal = (g["canal_dist"], -g["canal_dist"] / 2)
    hueco = local(0, g["r_int"] + g["hueco_prof"] / 2, 0)
    marcas = [
        (borde_derecho(zt), "Capa de arriba, EPS de 30 mm"),
        (proy(*centro_v, zt + CAPA), "Ventana de la caja estanca, tapa arriba"),
        (borde_derecho(zm), "Capa del medio"),
        (proy(*lado_canal, zm + CAPA), "Canal del cuadrado de carbono"),
        (proy(*hueco, zm + CAPA), "Hueco de mano"),
        (borde_derecho(za), "Capa de abajo, igual a la de arriba"),
        (proy(*centro_v, za + CAPA), "Tapón de 15 mm debajo de cada caja"),
    ]
    marcas.sort(key=lambda m: m[0][1])
    xt = max(p[0] for p in [proy(x, y, 0) for x, y in C["arriba"][0]]) + 70
    out, ultimo = [], -1e9
    for (px, py), txt in marcas:
        ty = max(py, ultimo + 30)
        ultimo = ty
        out.append(f'<path d="M {px:.1f} {py:.1f} L {xt - 14:.1f} {ty:.1f} L {xt - 6:.1f} {ty:.1f}" fill="none" '
                   f'stroke="{SEC}" stroke-width="0.8"/>')
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.6" fill="{C1}"/>')
        out.append(f'<text x="{xt:.1f}" y="{ty + 6:.1f}" font-size="19" fill="{C1}">{txt}</text>')
    todo = [proy(x, y, zz) for nombre, z in niveles for x, y in C[nombre][0][::6] for zz in (z, z + CAPA)]
    x0 = min(p[0] for p in todo) - 10
    y0 = min(min(p[1] for p in todo), min(m[0][1] for m in marcas)) - 20
    y1 = max(max(p[1] for p in todo), ultimo) + 20
    x1 = xt + 380
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}" '
                f'font-family="WS, Work Sans, sans-serif">\n')
        f.write("\n".join(o + out) + "\n</svg>\n")


def main():
    P = parametros()
    g = medidas(P)
    C, info = capas(g)
    lado = 2 * g["r_ext"]
    iguales = info["en_abajo"]
    salidas = [("capa_exterior", C["arriba"])] if iguales else [("capa_arriba", C["arriba"]), ("capa_abajo", C["abajo"])]
    salidas.append(("capa_media", C["media"]))
    for nombre, conts in salidas:
        svg(os.path.join(AQUI, nombre + ".svg"), conts, lado)
        dxf(os.path.join(AQUI, nombre + ".dxf"), conts)
    l, w = CAJA["largo"] + 2 * JUEGO_CAJA, CAJA["ancho"] + 2 * JUEGO_CAJA
    if info["tapon_alto"] > 0:
        svg(os.path.join(AQUI, "tapon_caja.svg"), [[(x - l / 2, y - w / 2) for x, y in C["tapon"][0]]], l)
        dxf(os.path.join(AQUI, "tapon_caja.dxf"), C["tapon"])
    esquema(os.path.join(AQUI, "cuerpo_armado.svg"), g, C)

    # superficie de espuma de cada capa y masa
    a_ext = area(C["arriba"][0])
    a_vent = sum(area(v) for v in C["ventanas"])
    a_ductos = sum(area(d) for d in C["arriba"][2:6])
    a_arriba = a_ext - area(C["arriba"][1]) - a_ductos - a_vent
    a_abajo = a_ext - area(C["abajo"][1]) - a_ductos - (a_vent if info["en_abajo"] else 0)
    a_media = (a_ext - area(C["afuera"]) - a_vent) + (area(C["adentro"]) - area(C["media"][3]))
    vol = (a_arriba + a_media + a_abajo) * CAPA * 1e-9
    vol_tapon = 2 * l * w * info["tapon_alto"] * 1e-9
    masa = (vol + vol_tapon) * RHO_EPS
    print(f"aro de {lado:.1f} mm, centro libre de {2 * g['r_int']:.1f} mm, agujeros de ducto de "
          f"{2 * g['r_agujero']:.1f} mm a {g['r_mid']:.0f} mm del centro")
    print(f"capas: {'exterior x2' if iguales else 'arriba y abajo'} y media, de {CAPA:.0f} mm")
    print(f"cajas de {CAJA['ancho']:.0f} x {CAJA['largo']:.0f} x {CAJA['alto']:.0f} mm a "
          f"{', '.join(f'{a:.0f}' for a in ANGULOS_CAJAS)} grados, ventana de {w:.0f} x {l:.0f} mm desde "
          f"{info['r0']:.1f} mm del centro, en {'las tres capas' if info['en_abajo'] else 'arriba y en el medio'}")
    if info["tapon_alto"] > 0:
        print(f"tapón de {info['tapon_alto']:.0f} mm debajo de cada caja, de {w:.0f} x {l:.0f} mm")
    print("paredes mínimas:")
    for nombre, val in revisar(g, C, info):
        marca = "  AVISO" if val < PARED_MIN else ""
        print(f"  {nombre}: {val:.1f} mm{marca}")
    print(f"espuma: {vol * 1000:.1f} L en las tres capas más {vol_tapon * 1000:.2f} L de tapones, "
          f"{masa:.2f} kg con EPS de {RHO_EPS:.0f} kg/m3 (aprox., a validar)")
    print(f"superficie por capa: arriba {a_arriba / 1e6:.3f} m2, media {a_media / 1e6:.3f} m2, "
          f"abajo {a_abajo / 1e6:.3f} m2")


if __name__ == "__main__":
    main()
