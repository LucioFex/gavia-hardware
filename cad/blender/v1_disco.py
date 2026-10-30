"""Concepto 1: Disco con baranda.

Canto rodado chato de espuma con cuatro ductos de 7 pulgadas y una baranda de agarre
alrededor, separada del cuerpo por un hueco para los dedos. Simétrico arriba y abajo:
si da vuelta, flota igual y se agarra igual. La cinta dorada se enrosca en la baranda.

blender.exe -b --python v1_disco.py
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
    "holgura_punta": 0.003,
    "radio_ductos": 0.175,  # del centro al eje de cada ducto
    "pared_ducto": 0.012,
    "alto": 0.090,
    "abombado": 0.010,
    "hueco_dedos": 0.040,  # entre cuerpo y baranda
    "radio_baranda": 0.018,  # 36 mm de diámetro, agarre de mano adulta y de chico
    "puentes": 8,
    "cinta_vueltas": 9,
    "cinta_ancho": 0.018,
})
r_hel = P["helice_pulg"] * 0.0254 / 2
r_ducto = r_hel + P["holgura_punta"]
r_cuerpo = P["radio_ductos"] + r_ducto + P["pared_ducto"]
R_bar = r_cuerpo + P["hueco_dedos"] + P["radio_baranda"]
P["punto_agarre"] = (0.0, R_bar, 0.0)


def construir(P, M):
    T = P["alto"]
    cuerpo = L.revolucion("cuerpo", L.perfil_disco(r_cuerpo, T, abombado=P["abombado"]), seg=128, mat=M["cuerpo"])
    baranda = L.revolucion("baranda", L.perfil_circulo(R_bar, 0, P["radio_baranda"], 24), seg=160, mat=M["cuerpo"])
    puentes = []
    for k in range(P["puentes"]):
        a = 2 * math.pi * (k + 0.5) / P["puentes"]
        rm = (r_cuerpo + R_bar) / 2
        puentes.append(L.caja("puente", (R_bar - r_cuerpo + 0.02, 0.026, 0.030),
                              (rm * math.cos(a), rm * math.sin(a), 0), rot=(0, 0, a)))
    ductos = []
    cort = []
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        x, y = P["radio_ductos"] * math.cos(a), P["radio_ductos"] * math.sin(a)
        ductos.append((x, y))
        cort.append(L.cilindro("corte", r_ducto, T * 3, (x, y, 0), seg=96))
    L.booleana(cuerpo, puentes + [baranda], "UNION")
    L.booleana(cuerpo, cort)
    cuerpo.name = "cuerpo"

    # interior de cada ducto: rejillas, motor, hélice y brazo desde el centro
    zr = T / 2 - 0.004
    for (x, y) in ductos:
        piezas = []
        for z in (zr, -zr):
            piezas += L.rejilla("rej", r_ducto - 0.001, z, P["abertura_rejilla"], P["alambre_rejilla"], M["carbon"])
        piezas += L.motor("mot", -0.004, M["carbon"], M["oro_canto"])
        piezas += L.helice("hel", 2 * r_hel, 0.014, M["secundario"])
        for p in piezas:
            p.location.x += x
            p.location.y += y
        L.tubo_entre("brazo", (0, 0, -0.012), (x, y, -0.012), 0.007, M["carbon"])

    # tapa estanca, baliza y ventana de cámara
    L.revolucion("junta", L.perfil_circulo(0.062, T / 2 + P["abombado"] - 0.0005, 0.0012, 8), seg=96, mat=M["secundario"])
    L.esfera("baliza", 0.016, (0, 0, T / 2 + P["abombado"]), M["baliza"], (1, 1, 0.55))
    L.esfera("camara", 0.018, (0, 0, -T / 2 - P["abombado"]), M["vidrio"], (1, 1, 0.4))

    L.cinta_toroide("cinta", R_bar, P["radio_baranda"], P["cinta_vueltas"], P["cinta_ancho"], M["oro"])

    zr_dist = zr - 0.014
    a = math.radians(14)
    return {
        "cuerpo": cuerpo,
        "ductos": ductos,
        "manos": [(-R_bar * math.sin(a), R_bar * math.cos(a), 0.02), (R_bar * math.sin(a), R_bar * math.cos(a), 0.02)],
        "envergadura": 2 * (R_bar + P["radio_baranda"]),
        "alto": T + 2 * P["abombado"],
        "dist_rejilla": zr_dist,
        "vol_no_espuma_l": 1.3,
    }


if __name__ == "__main__":
    L.correr("v1_disco", P, construir)
