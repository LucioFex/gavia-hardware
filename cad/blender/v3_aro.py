"""Concepto 3: Aro abierto.

Un salvavidas de verdad: aro ancho de espuma con cuatro ductos de 6 pulgadas metidos en el
propio aro y el centro libre, para que la persona pase los brazos por adentro como en un aro
SOLAS. La batería y la electrónica van en dos cápsulas estancas dentro del aro, enfrentadas.
La cinta dorada ondula por el canto exterior.

blender.exe -b --python v3_aro.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gavia_lib as L

P = dict(L.BASE)
P.update({
    "helice_pulg": 6,
    "kg_por_motor": 1.5,  # 6 pulgadas en 6S (aprox., a validar)
    "holgura_punta": 0.003,
    "pared_ducto": 0.020,
    "alto": 0.090,
    "radio_medio": 0.29,
    "cinta_ancho": 0.020,
    "masa_motor_kg": 0.045,
    "masa_helice_kg": 0.009,
    "masa_rejilla_kg": 0.022,
    "masa_frame_kg": 0.22,  # aro de carbono que rigidiza la espuma (aprox., a validar)
})
r_hel = P["helice_pulg"] * 0.0254 / 2
r_ducto = r_hel + P["holgura_punta"]
r_mid = P["radio_medio"]
r_int = r_mid - r_ducto - P["pared_ducto"]
r_ext = r_mid + r_ducto + P["pared_ducto"]
P["pos_bateria"] = (r_mid, 0.0, 0.0)
P["pos_caja"] = (-r_mid, 0.0, 0.0)
P["punto_agarre"] = (0.0, r_mid, 0.0)
P["agarres_extra"] = {"canto_exterior": (0.0, r_ext - 0.02, 0.0)}


def construir(P, M):
    T = P["alto"]
    aro = L.revolucion("cuerpo", L.perfil_estadio(r_int, r_ext, T), seg=160, mat=M["cuerpo"])
    ductos = []
    cort = []
    for k in range(4):
        a = math.pi / 4 + k * math.pi / 2
        x, y = r_mid * math.cos(a), r_mid * math.sin(a)
        ductos.append((x, y))
        cort.append(L.cilindro("corte", r_ducto, T * 3, (x, y, 0), seg=96))
    L.booleana(aro, cort)
    aro.name = "cuerpo"

    zr = T / 2 - 0.004
    for (x, y) in ductos:
        piezas = []
        for z in (zr, -zr):
            piezas += L.rejilla("rej", r_ducto - 0.001, z, P["abertura_rejilla"], P["alambre_rejilla"], M["carbon"])
        piezas += L.motor("mot", -0.004, M["carbon"], M["oro_canto"], tam=0.015)
        piezas += L.helice("hel", 2 * r_hel, 0.012, M["secundario"])
        for p in piezas:
            p.location.x += x
            p.location.y += y
        f = (r_mid - r_ducto) / r_mid
        L.tubo_entre("soporte", (x * f, y * f, -0.012), (x, y, -0.012), 0.006, M["carbon"])

    # tapas de las dos cápsulas, baliza arriba de la electrónica
    for x in (r_mid, -r_mid):
        j = L.revolucion("junta", L.perfil_circulo(0.05, T / 2 - 0.0005, 0.0012, 8), seg=64, mat=M["secundario"])
        j.location = (x, 0, 0)
    L.esfera("baliza", 0.016, (-r_mid, 0, T / 2), M["baliza"], (1, 1, 0.55))
    L.esfera("camara", 0.018, (-r_mid, 0, -T / 2), M["vidrio"], (1, 1, 0.4))
    L.cinta_toroide("cinta", r_ext - T / 2, T / 2, 0, P["cinta_ancho"], M["oro"], rango_v=(1.1, 5))
    return {
        "cuerpo": aro,
        "ductos": ductos,
        "manos": [(-0.11, r_int + 0.015, 0.04), (0.11, r_int + 0.015, 0.04)],
        "envergadura": 2 * r_ext,
        "alto": T,
        "dist_rejilla": zr - 0.012,
        "vol_no_espuma_l": 1.4,
    }


if __name__ == "__main__":
    L.correr("v3_aro", P, construir)
