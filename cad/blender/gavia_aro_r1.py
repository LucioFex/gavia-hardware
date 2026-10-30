"""Gavia, aro flotante. Ronda 1 de refinamiento del concepto 3 (v3_aro.py).

Cambios de la ronda 1, con lo que dijeron los críticos:
- Hélices de 7 pulgadas con liner rígido naranja y 5 mm de holgura, hélice centrada entre rejillas.
- Rejilla de flejes radiales con ranura de 5 mm y aro estructural, en gris cálido. Deja la rejilla
  de anillos y rayos, que es el lenguaje del TY-3R.
- Sección de canto recto (radio_canto) para que se lea moldeado y no inflable.
- Faja dorada de dos vueltas que envuelve la sección y cruza las caras entre los ductos, embutida.
- Cuerpo crema mate, oro satinado en el tono profundo, naranja solo dentro de los ductos.
- LiPo 6S y ESC en la misma cápsula, la otra cápsula lleva solo señal. Baliza al ras.
- k_ducto 1,0 hasta medir en banco, piel con peso más realista.

blender.exe -b --python gavia_aro_r1.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gavia_lib as L

P = dict(L.BASE)
P.update({
    "helice_pulg": 7,
    "kg_por_motor": 2.0,  # 7 pulgadas en 6S, empuje estático libre (aprox., a validar)
    "k_ducto": 1.0,  # sin ganancia hasta medir en banco (labio de canto vivo, holgura del 5 %)
    "k_rejilla": 0.85,  # dos rejillas de fleje alineado con el flujo (aprox., a validar)
    "holgura_punta": 0.005,
    "liner": 0.002,  # tubo rígido naranja dentro de la espuma
    "pared_ducto": 0.015,
    "alto": 0.090,
    "radio_medio": 0.29,
    "radio_canto": 0.030,
    "abertura_rejilla": 0.005,
    "fleje_espesor": 0.0015,
    "fleje_prof": 0.006,
    "cinta_vueltas": 2,
    "cinta_ancho": 0.030,
    "piel_kg_m2": 0.6,  # piel elástica de poliurea fina (aprox., a validar)
    "masa_frame_kg": 0.22,  # cuadrado de tubos de carbono que une los cuatro motores
    "masa_motor_kg": 0.055,
})
r_hel = P["helice_pulg"] * 0.0254 / 2
r_ducto = r_hel + P["holgura_punta"] + P["liner"]
r_mid = P["radio_medio"]
r_int = r_mid - r_ducto - P["pared_ducto"]
r_ext = r_mid + r_ducto + P["pared_ducto"]
P["pos_bateria"] = (r_mid, 0.0, 0.0)  # LiPo y ESC
P["pos_caja"] = (-r_mid, 0.0, 0.0)  # controladora, radios, computadora y cámara
P["punto_agarre"] = (0.0, r_mid, 0.0)
P["agarres_extra"] = {"canto_exterior": (0.0, r_ext - 0.02, 0.0), "canto_interior": (0.0, r_int + 0.02, 0.0)}


def perfil(P):
    return L.perfil_estadio(r_int, r_ext, P["alto"], radio=P["radio_canto"])


def construir(P, M):
    T = P["alto"]
    aro = L.revolucion("cuerpo", perfil(P), seg=192, mat=M["cuerpo"])
    ductos = []
    cort = []
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        x, y = r_mid * math.cos(a), r_mid * math.sin(a)
        ductos.append((x, y))
        cort.append(L.cilindro("corte", r_ducto, T * 3, (x, y, 0), seg=128))
    L.booleana(aro, cort)
    aro.name = "cuerpo"

    zr = T / 2 - P["fleje_prof"] / 2 - 0.001
    r_in = r_ducto - P["liner"]
    for (x, y) in ductos:
        ang = math.atan2(y, x)
        piezas = [L.revolucion("liner", L.perfil_estadio(r_in, r_ducto + 0.0005, T - 0.002, radio=0.0008),
                               seg=128, mat=M["ducto"])]
        for z in (zr, -zr):
            piezas += L.rejilla_fleje("rej", r_in - 0.0005, z, P["abertura_rejilla"], P["fleje_espesor"],
                                      P["fleje_prof"], M["rejilla"], angulo=ang)
        piezas += L.motor("mot", -0.012, M["carbon"], M["carbon"])
        piezas += L.helice("hel", 2 * r_hel, 0.0, M["secundario"])
        for p in piezas:
            p.location.x += x
            p.location.y += y
        f = (r_mid - r_in) / r_mid
        L.tubo_entre("soporte", (x * f, y * f, -0.02), (x, y, -0.02), 0.006, M["carbon"])

    # tapas al ras: una línea de junta apenas visible y la baliza como lente enrasada
    for x in (r_mid, -r_mid):
        j = L.revolucion("junta", L.perfil_circulo(0.05, T / 2, 0.0008, 8), seg=64, mat=M["linea"])
        j.location = (x, 0, 0)
    baliza = L.cilindro("baliza", 0.02, 0.003, (-r_mid, 0, T / 2 - 0.0005), mat=M["baliza_lente"])
    L.cilindro("camara", 0.014, 0.003, (-r_mid + 0.06, 0, -T / 2 + 0.0005), mat=M["vidrio"])

    # la faja cruza la cara de arriba en 90 y 270 grados y la de abajo en 0 y 180, entre los ductos
    pts, acum = L._arco_perfil(perfil(P))
    Ls = acum[-1]
    # punto medio de la cara superior: el tramo recto más largo con z en el tope
    h = P["alto"] / 2
    i_top = max((i for i in range(len(pts) - 1) if pts[i][1] > h - 1e-6 and pts[i + 1][1] > h - 1e-6),
                key=lambda i: acum[i + 1] - acum[i])
    s_top = (acum[i_top] + acum[i_top + 1]) / 2
    v = P["cinta_vueltas"]
    s0 = s_top - v * Ls * 0.25  # en u = 90 grados queda arriba
    L.cinta_perfil("cinta", perfil(P), v, P["cinta_ancho"], M["oro"], s0=s0)

    return {
        "cuerpo": aro,
        "ductos": ductos,
        "manos": [(-0.11, r_int + 0.015, 0.04), (0.11, r_int + 0.015, 0.04)],
        "envergadura": 2 * r_ext,
        "alto": T,
        "dist_rejilla": zr - P["fleje_prof"] / 2,
        "vol_no_espuma_l": 1.4,
        "baliza": baliza,
    }


if __name__ == "__main__":
    L.correr("gavia_aro_r1", P, construir, materiales=L.mats_r1)
