"""Gavia, aro flotante. Ronda 2 de refinamiento (sobre gavia_aro_r1.py).

Cambios de la ronda 2, con lo que dijeron los críticos:
- Hélices de 8 pulgadas con radio_medio 0,276: el aro queda en 800 mm y gana empuje y viento.
- Rejillas naranjas (el color funcional de los salvavidas) con tres nervios: ningún fleje queda
  suelto más de unos 50 mm, así un dedo no abre la ranura.
- Cuatro huecos de mano en el canto interior, que es el agarre que más aguanta.
- Faja dorada de 42 mm que cruza rápido las caras entre los ductos y se demora en las paredes.
- Sin líneas de junta, baliza como lente humo que se ve solo encendida, canto de 20 mm.
- Masa con los liners de los ductos y sin piel adentro de ellos.

blender.exe -b --python gavia_aro_r2.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gavia_lib as L

NOMBRE = "gavia_aro_r2"
P = dict(L.BASE)
P.update({
    "helice_pulg": 8,
    "kg_por_motor": 2.5,  # 8 pulgadas en 6S, empuje estático libre (aprox., a validar en banco)
    "k_ducto": 1.0,  # sin ganancia hasta medir (labio de canto vivo)
    "k_rejilla": 0.85,  # dos rejillas de fleje alineado con el flujo (aprox., a validar)
    "holgura_punta": 0.005,
    "liner": 0.002,  # tubo rígido dentro de la espuma
    "pared_ducto": 0.015,
    "alto": 0.090,
    "radio_medio": 0.276,
    "radio_canto": 0.020,
    "abertura_rejilla": 0.005,
    "fleje_espesor": 0.002,
    "fleje_prof": 0.006,
    "nervios_rejilla": 3,
    "huecos_mano": 4,
    "hueco_largo": 0.11,
    "hueco_alto": 0.034,
    "hueco_prof": 0.020,
    "cinta_vueltas": 2,
    "cinta_ancho": 0.042,
    "cinta_acel": 0.55,
    "piel_kg_m2": 0.6,  # piel elástica de poliurea fina (aprox., a validar con ensayo de golpe y UV)
    "masa_frame_kg": 0.22,  # cuadrado de tubos de carbono que une los cuatro motores
    "masa_motor_kg": 0.075,
    "masa_helice_kg": 0.015,
    "masa_rejilla_kg": 0.035,
    "masa_liner_kg": 0.07,
    "masa_bateria_kg": 0.48,  # LiPo 6S 3000 mAh: con 2200 no alcanza en ráfaga (crítica de la ronda 1)
})
r_hel = P["helice_pulg"] * 0.0254 / 2
r_ducto = r_hel + P["holgura_punta"] + P["liner"]
r_mid = P["radio_medio"]
r_int = r_mid - r_ducto - P["pared_ducto"]
r_ext = r_mid + r_ducto + P["pared_ducto"]
P["pos_bateria"] = (r_mid, 0.0, 0.0)  # LiPo y ESC, en un cajón que entra por el canto exterior
P["pos_caja"] = (-r_mid, 0.0, 0.0)  # controladora, radios, computadora, cámara y corte por agua
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
    # huecos de mano en el canto interior, entre los ductos
    for k in range(P["huecos_mano"]):
        a = k * 2 * math.pi / P["huecos_mano"]
        rc = r_int + P["hueco_prof"] / 2 - 0.01
        c = L.caja("hueco", (P["hueco_largo"], P["hueco_prof"] + 0.02, P["hueco_alto"]),
                   (rc * math.cos(a), rc * math.sin(a), 0), rot=(0, 0, a + math.pi / 2))
        bv = c.modifiers.new("bisel", "BEVEL")
        bv.width = 0.009
        bv.segments = 5
        L.aplicar(c)
        cort.append(c)
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
                                      P["fleje_prof"], M["rejilla"], angulo=ang, nervios=P["nervios_rejilla"])
        piezas += L.motor("mot", -0.012, M["carbon"], M["carbon"], tam=0.019)
        piezas += L.helice("hel", 2 * r_hel, 0.0, M["secundario"])
        for p in piezas:
            p.location.x += x
            p.location.y += y
        f = (r_mid - r_in) / r_mid
        L.tubo_entre("soporte", (x * f, y * f, -0.02), (x, y, -0.02), 0.006, M["carbon"])

    baliza = L.cilindro("baliza", 0.02, 0.003, (-r_mid, 0, T / 2 - 0.0005), mat=M["baliza_lente"])
    L.cilindro("camara", 0.014, 0.003, (-r_mid + 0.06, 0, -T / 2 + 0.0005), mat=M["vidrio"])

    # la faja cruza la cara de arriba en 90 y 270 grados y la de abajo en 0 y 180, entre los ductos
    pts, acum = L._arco_perfil(perfil(P))
    Ls = acum[-1]
    h = T / 2
    i_top = max((i for i in range(len(pts) - 1) if pts[i][1] > h - 1e-6 and pts[i + 1][1] > h - 1e-6),
                key=lambda i: acum[i + 1] - acum[i])
    s_top = (acum[i_top] + acum[i_top + 1]) / 2
    v = P["cinta_vueltas"]
    L.cinta_perfil("cinta", perfil(P), v, P["cinta_ancho"], M["oro"], s0=s_top - v * Ls * 0.25,
                   s_cara=s_top, acel=P["cinta_acel"])

    masa_extra = [(f"liner ducto {i + 1}", P["masa_liner_kg"], (x, y, 0.0), "tubo de 2 mm (aprox., a validar)")
                  for i, (x, y) in enumerate(ductos)]
    return {
        "cuerpo": aro,
        "ductos": ductos,
        "manos": [(-0.05, r_int + 0.01, 0.0), (0.05, r_int + 0.01, 0.0)],
        "envergadura": 2 * r_ext,
        "alto": T,
        "dist_rejilla": zr - P["fleje_prof"] / 2,
        "vol_no_espuma_l": 1.4,
        "baliza": baliza,
        "masa_extra": masa_extra,
        "area_sin_piel_m2": 4 * 2 * math.pi * r_ducto * T,
    }


if __name__ == "__main__":
    L.correr(NOMBRE, P, construir, materiales=L.mats_r1)
