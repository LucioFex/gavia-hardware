"""Concepto 2: Cruz de brazos flotantes.

Un cubo central estanco con la batería y la electrónica, cuatro brazos flotantes que se
abrazan como un rescue tube y cuatro ductos livianos en las puntas. Configuración en +:
un brazo siempre apunta hacia la persona. La cinta dorada ondula alrededor del cubo.

blender.exe -b --python v2_cruz.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gavia_lib as L

P = dict(L.BASE)
P.update({
    "helice_pulg": 7,
    "kg_por_motor": 2.0,  # 7 pulgadas en 6S (aprox., a validar)
    "holgura_punta": 0.003,
    "radio_ductos": 0.34,
    "pared_ducto": 0.024,
    "alto_ducto": 0.080,
    "radio_cubo": 0.11,
    "alto_cubo": 0.13,
    "radio_brazo": 0.050,  # 100 mm, se abraza como un rescue tube
    "cinta_ancho": 0.020,
})
r_hel = P["helice_pulg"] * 0.0254 / 2
r_ducto = r_hel + P["holgura_punta"]
y_agarre = (P["radio_cubo"] + P["radio_ductos"] - r_ducto) / 2 + 0.02
P["punto_agarre"] = (0.0, y_agarre, 0.0)
P["agarres_extra"] = {"collar": (0.0, P["radio_ductos"] + r_ducto + P["pared_ducto"], 0.0)}


def construir(P, M):
    Rc, Hc = P["radio_cubo"], P["alto_cubo"]
    cubo = L.revolucion("cubo", L.perfil_disco(Rc, Hc), seg=96, mat=M["cuerpo"])
    partes = []
    ductos = []
    for k in range(4):
        a = k * math.pi / 2
        c, s = math.cos(a), math.sin(a)
        x, y = P["radio_ductos"] * c, P["radio_ductos"] * s
        ductos.append((x, y))
        r0 = Rc * 0.5
        r1 = P["radio_ductos"] - r_ducto - 0.005
        partes.append(L.tubo_entre("brazo", (r0 * c, r0 * s, 0), (r1 * c, r1 * s, 0), P["radio_brazo"], seg=48))
        col = L.revolucion("collar", L.perfil_estadio(r_ducto, r_ducto + P["pared_ducto"], P["alto_ducto"]), seg=96)
        col.location = (x, y, 0)
        partes.append(col)
    cuerpo = L.unir([cubo] + partes, "cuerpo")
    cuerpo.data.materials.clear()
    cuerpo.data.materials.append(M["cuerpo"])

    zr = P["alto_ducto"] / 2 - 0.004
    for (x, y) in ductos:
        piezas = []
        for z in (zr, -zr):
            piezas += L.rejilla("rej", r_ducto - 0.001, z, P["abertura_rejilla"], P["alambre_rejilla"], M["carbon"])
        piezas += L.motor("mot", -0.004, M["carbon"], M["oro_canto"])
        piezas += L.helice("hel", 2 * r_hel, 0.012, M["secundario"])
        for p in piezas:
            p.location.x += x
            p.location.y += y
        f = 1 - r_ducto / P["radio_ductos"]
        L.tubo_entre("soporte", (x * f, y * f, -0.012), (x, y, -0.012), 0.006, M["carbon"])

    L.revolucion("junta", L.perfil_circulo(0.07, Hc / 2 - 0.0005, 0.0012, 8), seg=96, mat=M["secundario"])
    L.esfera("baliza", 0.018, (0, 0, Hc / 2), M["baliza"], (1, 1, 0.55))
    L.esfera("camara", 0.02, (0, 0, -Hc / 2), M["vidrio"], (1, 1, 0.4))
    # la cinta pasa por arriba de los brazos y baja entre ellos
    L.cinta_toroide("cinta", Rc - Hc / 2, Hc / 2, 0, P["cinta_ancho"], M["oro"], rango_v=(1.05, 4), fase=math.pi / 2)
    return {
        "cuerpo": cuerpo,
        "ductos": ductos,
        "manos": [(-0.07, y_agarre, 0.035), (0.07, y_agarre, 0.035)],
        "envergadura": 2 * (P["radio_ductos"] + r_ducto + P["pared_ducto"]),
        "alto": Hc,
        "dist_rejilla": zr - 0.012,
        "vol_no_espuma_l": 1.5,
    }


if __name__ == "__main__":
    L.correr("v2_cruz", P, construir)
