"""Gavia, botonera del guardavidas. Diseño de la sesión del 2026-10-30.

Una caja estanca comercial en crema, fija al puesto, con la pantallita arriba y los dos botones
grandes de D-011 abajo: INCIDENTE REAL en rojo fuerte y FALSO POSITIVO en gris. Se arma entre
tres personas sin impresora 3D, con piezas que se compran hechas:

- Caja estanca IP65 de ABS de 200 x 120 x 75 mm con tapa atornillada en las cuatro esquinas.
- Dos pulsadores industriales de 30 mm con aro protector, así un golpe no los aprieta.
- Pantalla OLED de 1,3 pulgadas detrás de una ventana, LED de estado y buzzer.
- Un solo cable USB-C a la laptop, que la alimenta y lleva los mensajes. Sale por un prensacable
  al costado, sin pila adentro.
- Dos orejas arriba y abajo para atornillarla al poste del puesto.

Los rótulos van grabados y rellenos con tinta carbón. En la tapa, solo "Gavia" chica.
Todas las medidas son de piezas comerciales típicas (aprox., a validar con la pieza en mano).

blender.exe -b --python gavia_botonera.py
"""
import math
import os
import sys

import bpy
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gavia_lib as L

NOMBRE = "gavia_botonera"
FUENTES = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts")

P = {
    # caja estanca IP65 de ABS, tamaño de catálogo (aprox., a validar)
    "ancho": 0.120,
    "alto": 0.200,
    "fondo": 0.075,
    "tapa": 0.016,  # espesor de la tapa, el resto es el cuerpo
    "junta": 0.0006,  # línea entre tapa y cuerpo
    "radio_canto": 0.005,
    "tornillo_offset": 0.010,  # tornillos de la tapa, desde cada esquina
    # orejas de fijación al poste, arriba y abajo (aprox., a validar)
    "oreja_ancho": 0.040,
    "oreja_alto": 0.020,
    "oreja_espesor": 0.004,
    # pulsador industrial de 30 mm con aro protector (aprox., a validar)
    "boton_diam": 0.030,
    "aro_diam": 0.044,
    "aro_alto": 0.009,  # el aro queda más alto que el botón: un golpe no lo aprieta
    "boton_alto": 0.006,
    "boton_z": (0.029, -0.037),  # INCIDENTE REAL arriba, FALSO POSITIVO abajo
    # pantalla OLED de 1,3 pulgadas, 128 x 64 (aprox., a validar)
    "ventana": (0.040, 0.024),
    "ventana_z": 0.076,
    "led_diam": 0.005,
    "buzzer_diam": 0.004,
    # prensacable PG7 para el cable USB-C (aprox., a validar)
    "prensa_diam": 0.015,
    "prensa_z": -0.072,
    "cable_diam": 0.004,
    # rótulos
    "rotulo_alto": 0.0052,  # alto de mayúscula
    "marca_alto": 0.0062,
    "res": 1400,
}

ROJO = "#C62A20"  # rojo fuerte de D-011, a definir con Elías
GRIS = "#9A938A"  # gris cálido, de la familia de la paleta


def mats():
    M = L.mats()
    M["caja"] = L.material("caja_crema", "crema", rough=0.58)
    M["rojo"] = L.material("boton_rojo", ROJO, rough=0.38, coat=0.2)
    M["gris"] = L.material("boton_gris", GRIS, rough=0.42, coat=0.2)
    M["aro"] = L.material("aro_carbon", "carbon", rough=0.5)
    M["tinta"] = L.material("tinta_carbon", "carbon", rough=0.65)
    M["pantalla"] = L.material("pantalla", "#0B0D0F", rough=0.12)
    M["pixel"] = L.material("pixel", "crema_claro", rough=0.4, emit=3.0)
    M["led"] = L.material("led", "naranja", rough=0.2, emit=2.2)
    M["agujero"] = L.material("agujero", "#141414", rough=0.9)
    M["madera"] = L.material("madera", "#A98B68", rough=0.8)
    M["arena"] = L.material("arena", "#E2D6BE", rough=0.95)
    M["acero"] = L.material("acero", "#8C8A86", rough=0.35, metal=0.8)
    M["pared"] = L.material("pared", "linea", rough=0.9)
    return M


def caja_redonda(nombre, dims, pos, radio, mat):
    ob = L.caja(nombre, dims, pos, mat)
    b = ob.modifiers.new("canto", "BEVEL")
    b.width = radio
    b.segments = 5
    b.limit_method = "ANGLE"
    L.aplicar(ob)
    L.suavizar(ob, 35)
    return ob


def disco_frente(nombre, radio, prof, x, z, y_cara, mat, seg=64):
    """Cilindro con el eje en Y, apoyado en la cara frontal (y_cara) y saliendo hacia -Y."""
    return L.cilindro(nombre, radio, prof, pos=(x, y_cara - prof / 2, z), seg=seg, mat=mat,
                      rot=(math.radians(90), 0, 0))


def texto(nombre, cuerpo, alto_mayus, fuente, mat, pos, rot=(math.radians(90), 0, 0), ext=0.00012,
          ancho_max=None):
    cu = bpy.data.curves.new(nombre, "FONT")
    cu.body = cuerpo
    cu.font = bpy.data.fonts.load(os.path.join(FUENTES, fuente), check_existing=True)
    cu.size = alto_mayus / 0.66  # Work Sans: la mayúscula mide unos 0,66 del cuerpo
    cu.extrude = ext
    cu.align_x = "CENTER"
    cu.align_y = "CENTER"
    ob = bpy.data.objects.new(nombre, cu)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    ob.location = pos
    ob.rotation_euler = rot
    if ancho_max:
        bpy.context.view_layer.update()
        if ob.dimensions.x > ancho_max:
            cu.size *= ancho_max / ob.dimensions.x
    return ob


def construir(M):
    a, h, f, t = P["ancho"], P["alto"], P["fondo"], P["tapa"]
    y_frente = -f  # el fondo de la caja apoya en y = 0, el frente mira a -Y
    piezas = []

    # cuerpo y tapa, separados por la junta
    cuerpo = caja_redonda("cuerpo", (a, f - t, h), (0, -(f - t) / 2, 0), P["radio_canto"], M["caja"])
    tapa = caja_redonda("tapa", (a, t - P["junta"], h), (0, -(f - t) - (t - P["junta"]) / 2 - P["junta"], 0),
                        P["radio_canto"], M["caja"])

    # agujeros de la tapa: botones, ventana, LED, buzzer y cabezas de tornillo
    cortes = []
    for z in P["boton_z"]:
        cortes.append(disco_frente("c_boton", P["boton_diam"] / 2 + 0.0005, 0.03, 0, z, y_frente + 0.02, None))
    vx, vz = P["ventana"]
    cortes.append(L.caja("c_ventana", (vx, 0.006, vz), (0, y_frente + 0.0015, P["ventana_z"])))
    x_led = a / 2 - 0.018
    cortes.append(disco_frente("c_led", 0.004, 0.03, x_led, P["ventana_z"], y_frente + 0.02, None, 32))
    cortes.append(disco_frente("c_buzzer", P["buzzer_diam"] / 2, 0.03, -x_led, P["ventana_z"], y_frente + 0.02,
                               None, 32))
    o = P["tornillo_offset"]
    tornillos = [(sx * (a / 2 - o), sz * (h / 2 - o)) for sx in (-1, 1) for sz in (-1, 1)]
    for x, z in tornillos:
        cortes.append(disco_frente("c_tornillo", 0.004, 0.002, x, z, y_frente + 0.001, None, 32))
    L.booleana(tapa, cortes)
    L.suavizar(tapa, 35)
    piezas += [cuerpo, tapa]

    # tornillos de la tapa, hundidos en su alojamiento
    for x, z in tornillos:
        tor = disco_frente("tornillo", 0.0032, 0.0015, x, z, y_frente + 0.0018, M["acero"], 24)
        ranura = L.caja("ranura", (0.0045, 0.0006, 0.0008), (x, y_frente + 0.0003, z), M["agujero"])
        piezas += [tor, ranura]

    # pantalla OLED detrás de la ventana, con las dos líneas de 09_botonera.md
    pantalla = L.caja("pantalla", (vx - 0.002, 0.002, vz - 0.002), (0, y_frente + 0.0028, P["ventana_z"]),
                      M["pantalla"])
    piezas.append(pantalla)
    y_px = y_frente + 0.0017
    texto("pantalla_1", "78% · Sector 3", 0.0042, "WorkSans-SemiBold.ttf", M["pixel"],
          (0, y_px, P["ventana_z"] + 0.0042), ancho_max=vx - 0.008)
    texto("pantalla_2", "Suelta en 15 s", 0.0034, "WorkSans-Medium.ttf", M["pixel"],
          (0, y_px, P["ventana_z"] - 0.0046), ancho_max=vx - 0.012)

    # LED de estado con su bisel, y el buzzer como un agujero oscuro
    piezas.append(disco_frente("led_bisel", 0.0046, 0.0012, x_led, P["ventana_z"], y_frente, M["aro"], 32))
    led = L.esfera("led", P["led_diam"] / 2, (x_led, y_frente - 0.0008, P["ventana_z"]), M["led"],
                   (1, 0.55, 1))
    piezas.append(led)
    piezas.append(disco_frente("buzzer", P["buzzer_diam"] / 2, 0.0005, -x_led, P["ventana_z"], y_frente + 0.004,
                               M["agujero"], 32))

    # pulsadores: aro protector en carbón y botón un poco hundido
    for z, mat, rotulo in ((P["boton_z"][0], M["rojo"], "INCIDENTE REAL"),
                           (P["boton_z"][1], M["gris"], "FALSO POSITIVO")):
        aro = disco_frente("aro", P["aro_diam"] / 2, P["aro_alto"], 0, z, y_frente, M["aro"], 72)
        hueco = disco_frente("aro_hueco", P["boton_diam"] / 2 + 0.0015, P["aro_alto"] + 0.002, 0, z,
                             y_frente + 0.001, None, 72)
        L.booleana(aro, [hueco])
        canto = aro.modifiers.new("canto", "BEVEL")
        canto.width = 0.0012
        canto.segments = 3
        canto.limit_method = "ANGLE"
        L.aplicar(aro)
        L.suavizar(aro, 35)
        boton = disco_frente("boton", P["boton_diam"] / 2, P["boton_alto"], 0, z, y_frente, mat, 72)
        b = boton.modifiers.new("canto", "BEVEL")
        b.width = 0.0022
        b.segments = 5
        b.limit_method = "ANGLE"
        L.aplicar(boton)
        L.suavizar(boton, 60)
        piezas += [aro, boton]
        texto(f"rotulo_{rotulo}", rotulo, P["rotulo_alto"], "WorkSans-Bold.ttf", M["tinta"],
              (0, y_frente - 0.00002, z - P["aro_diam"] / 2 - 0.0085), ancho_max=a - 0.03)

    texto("marca", "Gavia", P["marca_alto"], "WorkSans-ExtraBold.ttf", M["tinta"],
          (0, y_frente - 0.00002, -h / 2 + 0.013))

    # orejas de fijación, contra el fondo de la caja, arriba y abajo
    for sz in (1, -1):
        oreja = caja_redonda("oreja", (P["oreja_ancho"], P["oreja_espesor"], P["oreja_alto"] + 0.012),
                             (0, -P["oreja_espesor"] / 2, sz * (h / 2 + P["oreja_alto"] / 2 - 0.006)), 0.0018,
                             M["caja"])
        ojal = L.caja("ojal", (0.0055, 0.02, 0.011), (0, 0, sz * (h / 2 + P["oreja_alto"] / 2)))
        L.booleana(oreja, [ojal])
        L.suavizar(oreja, 35)
        piezas.append(oreja)

    # prensacable PG7 en el costado derecho, cerca de abajo, y el cable USB-C que baja
    x_lado = a / 2
    y_pr = -(f - t) / 2
    tuerca = L.cilindro("prensa_tuerca", P["prensa_diam"] / 2, 0.006, (x_lado + 0.003, y_pr, P["prensa_z"]), seg=6,
                        mat=M["aro"], rot=(0, math.radians(90), 0))
    domo = L.cilindro("prensa_domo", 0.0062, 0.010, (x_lado + 0.011, y_pr, P["prensa_z"]), seg=32, mat=M["aro"],
                      rot=(0, math.radians(90), 0))
    L.suavizar(domo, 60)
    piezas += [tuerca, domo]
    return {"piezas": piezas, "y_frente": y_frente, "x_cable": x_lado + 0.016, "y_cable": y_pr}


def cable(nombre, puntos, radio, mat):
    cu = bpy.data.curves.new(nombre, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radio
    cu.bevel_resolution = 4
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(puntos) - 1)
    for bp, p in zip(sp.bezier_points, puntos):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    ob = bpy.data.objects.new(nombre, cu)
    bpy.context.scene.collection.objects.link(ob)
    ob.data.materials.append(mat)
    return ob


def main():
    L.limpiar()
    L.preparar_render(P["res"])
    M = mats()
    g = construir(M)
    xc, yc, zc = g["x_cable"], g["y_cable"], P["prensa_z"]

    # la botonera en la pared, para las vistas de producto
    raiz = bpy.data.objects.new("botonera", None)
    bpy.context.scene.collection.objects.link(raiz)
    for ob in bpy.context.scene.objects:
        if ob is not raiz and ob.parent is None and ob.type in ("MESH", "FONT"):
            ob.parent = raiz
    L.luces()
    sol = bpy.data.objects["sol"]
    sol.rotation_euler = (math.radians(58), 0, math.radians(-28))  # luz rasante desde adelante y arriba
    sol.data.energy = 1.7  # sin quemar el crema de la tapa
    pared = L.caja("pared", (3, 0.01, 3), (0, 0.005, 0), M["pared"])
    cab = cable("cable", [(xc, yc, zc), (xc + 0.02, yc, zc - 0.01), (xc + 0.028, yc + 0.004, zc - 0.06),
                          (xc + 0.03, yc + 0.01, -0.4)], P["cable_diam"] / 2, M["carbon"])

    carpeta = os.path.join(L.HERE, "renders", NOMBRE)
    os.makedirs(carpeta, exist_ok=True)
    L.render(L.camara("c34", (0.004, -0.03, 0.0), -62, 16, 0.78, lente=70), os.path.join(carpeta, "1_tres_cuartos.png"))
    L.render(L.camara("cfr", (0, -0.03, 0.0), -90, 0, 0.82, lente=70), os.path.join(carpeta, "2_frente.png"))

    # en el puesto: atornillada a un poste de madera, con el cable que baja hacia la laptop
    bpy.data.objects.remove(pared, do_unlink=True)
    bpy.data.objects.remove(cab, do_unlink=True)
    z_caja = 1.25
    lado_poste = 0.10
    raiz.location = (0, -0.0005, z_caja)
    L.caja("poste", (lado_poste, lado_poste, 2.4), (0, lado_poste / 2, 1.2), M["madera"])
    L.cilindro("piso", 30, 0.01, (0, 0, -0.005), mat=M["arena"])
    x_baja = lado_poste / 2 - 0.006  # el cable baja pegado a la cara del poste, sin meterse adentro
    cable("cable_poste", [(xc, yc, z_caja + zc), (xc + 0.012, yc, z_caja + zc - 0.03),
                          (x_baja, -0.008, z_caja - 0.22), (x_baja, -0.008, 0.6), (x_baja, -0.008, 0.02)],
          P["cable_diam"] / 2, M["carbon"])
    for sz in (1, -1):  # tornillos de las orejas
        L.cilindro("tornillo_oreja", 0.0045, 0.002, (0, -P["oreja_espesor"] - 0.001,
                                                       z_caja + sz * (P["alto"] / 2 + P["oreja_alto"] / 2)),
                   seg=24, mat=M["acero"], rot=(math.radians(90), 0, 0))
    L.render(L.camara("ctorre", (0.0, -0.02, z_caja - 0.12), -60, 10, 1.25, lente=50),
             os.path.join(carpeta, "3_en_la_torre.png"))

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(L.HERE, f"{NOMBRE}.blend"))
    print("BOTONERA", {k: P[k] for k in ("ancho", "alto", "fondo", "boton_diam", "aro_diam")})


main()
