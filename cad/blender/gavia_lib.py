"""Librería común de los conceptos del dron flotador Gavia.

Geometría paramétrica (revoluciones, tubos, booleanas), materiales con la paleta,
escenas y renders, y la ficha de física: hidrostática por vóxeles, escora con un
adulto agarrado de un lado, curva de adrizamiento, área al viento y empuje.

Uso: blender.exe -b --python v1_disco.py
Todos los números de entrada sin fuente van marcados como aprox., a validar
en la ficha JSON que se escribe junto a los renders.
"""
import bpy
import bmesh
import json
import math
import os
from mathutils import Vector, Matrix
from mathutils.bvhtree import BVHTree
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- paleta
# sRGB. Paleta de Gavia: crema y carbón, nunca blanco puro. Tres oros para la faja:
# la masa en el profundo, el canto en el base y la luz en el claro.
PALETA = {
    "crema": "#F8F4EB",
    "crema_claro": "#FFFDF8",
    "carbon": "#1F1F1F",
    "secundario": "#5C534A",
    "linea": "#D9CFC0",
    "oro": "#C9AD64",
    "oro_claro": "#DCC488",
    "oro_profundo": "#A8894A",
    "naranja": "#F26B1D",  # candidato a acento de Gavia, hex a definir con Elías
    "piel": "#A39A90",  # maniquí gris arcilla, neutro
    "agua": "#2F5D63",
    "fondo": "#ECE6DA",
}

# ---------------------------------------------------------------- física
RHO_MAR = 1025.0  # kg/m3, agua de mar (informe de la wiki, aprox.)
RHO_AIRE = 1.225  # kg/m3 al nivel del mar
G = 9.81


def srgb_to_linear(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


# ---------------------------------------------------------------- escena
def limpiar():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def material(nombre, color, rough=0.5, metal=0.0, emit=0.0, coat=0.0, alpha=1.0):
    m = bpy.data.materials.get(nombre)
    if m:
        return m
    m = bpy.data.materials.new(nombre)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    col = srgb_to_linear(PALETA.get(color, color))
    p.inputs["Base Color"].default_value = col
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    if coat:
        p.inputs["Coat Weight"].default_value = coat
    if emit:
        p.inputs["Emission Color"].default_value = col
        p.inputs["Emission Strength"].default_value = emit
    if alpha < 1:
        p.inputs["Alpha"].default_value = alpha
    return m


def mats():
    return {
        "cuerpo": material("cuerpo", "crema", rough=0.42, coat=0.15),
        "cuerpo_claro": material("cuerpo_claro", "crema_claro", rough=0.4),
        "oro": material("oro", "oro_profundo", rough=0.32, metal=0.75),
        "oro_canto": material("oro_canto", "oro", rough=0.28, metal=0.8),
        "carbon": material("carbon", "carbon", rough=0.55),
        "secundario": material("secundario", "secundario", rough=0.5),
        "vidrio": material("vidrio", "#101418", rough=0.05, metal=0.2),
        "baliza": material("baliza", "naranja", rough=0.3, emit=2.5),
        "naranja": material("naranja", "naranja", rough=0.45),
        "piel": material("piel", "piel", rough=0.7),
        "agua": material("agua", "agua", rough=0.08),
        "fondo": material("fondo", "fondo", rough=0.9),
    }


def objeto(nombre, me, mat=None, parent=None):
    ob = bpy.data.objects.new(nombre, me)
    bpy.context.scene.collection.objects.link(ob)
    if mat:
        ob.data.materials.append(mat)
    if parent:
        ob.parent = parent
    return ob


def suavizar(ob, angulo=40):
    for p in ob.data.polygons:
        p.use_smooth = True
    try:
        ob.data.set_sharp_from_angle(angle=math.radians(angulo))
    except Exception:
        pass


# ---------------------------------------------------------------- geometría
def revolucion(nombre, perfil, seg=96, mat=None, cerrado=True):
    """Revoluciona un perfil [(r, z), ...] alrededor de Z. Los puntos con r=0 se sueldan."""
    bm = bmesh.new()
    filas = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        ca, sa = math.cos(a), math.sin(a)
        filas.append([bm.verts.new((r * ca, r * sa, z)) for r, z in perfil])
    n = len(perfil)
    lim = n if cerrado else n - 1
    for i in range(seg):
        f0, f1 = filas[i], filas[(i + 1) % seg]
        for j in range(lim):
            k = (j + 1) % n
            try:
                bm.faces.new((f0[j], f1[j], f1[k], f0[k]))
            except ValueError:
                pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    # caras degeneradas en los polos
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    ob = objeto(nombre, me, mat)
    suavizar(ob)
    return ob


def perfil_estadio(r_int, r_ext, alto, n=12, radio=None):
    """Sección de aro: rectángulo de esquinas redondeadas entre r_int y r_ext.
    Con radio=None las esquinas son lo más redondas posible (estadio si el ancho lo permite)."""
    rr = radio if radio is not None else min(alto, r_ext - r_int) / 2 * 0.999
    h = alto / 2
    esquinas = [(r_ext - rr, -h + rr, -math.pi / 2), (r_ext - rr, h - rr, 0.0),
                (r_int + rr, h - rr, math.pi / 2), (r_int + rr, -h + rr, math.pi)]
    pts = []
    for cx, cz, a0 in esquinas:
        for i in range(n + 1):
            a = a0 + (math.pi / 2) * i / n
            pts.append((cx + rr * math.cos(a), cz + rr * math.sin(a)))
    return pts


def perfil_disco(radio, alto, n=24, abombado=0.0):
    """Disco macizo con canto redondeado completo. abombado suma altura al centro."""
    h = alto / 2
    cx = radio - h
    pts = [(0.0, -h - abombado)]
    m = 12
    for i in range(1, m):
        r = cx * i / m
        pts.append((r, -h - abombado * (1 - (r / cx) ** 2)))
    for i in range(n + 1):
        a = -math.pi / 2 + math.pi * i / n
        pts.append((cx + h * math.cos(a), h * math.sin(a)))
    for i in range(m - 1, 0, -1):
        r = cx * i / m
        pts.append((r, h + abombado * (1 - (r / cx) ** 2)))
    pts.append((0.0, h + abombado))
    return pts


def perfil_circulo(rc, zc, r, n=16):
    return [(rc + r * math.cos(2 * math.pi * i / n), zc + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def cilindro(nombre, radio, alto, pos=(0, 0, 0), seg=64, mat=None, rot=None):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg,
                          radius1=radio, radius2=radio, depth=alto)
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    ob = objeto(nombre, me, mat)
    ob.location = pos
    if rot:
        ob.rotation_euler = rot
    return ob


def caja(nombre, dims, pos=(0, 0, 0), mat=None, rot=None):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = Vector((v.co.x * dims[0], v.co.y * dims[1], v.co.z * dims[2]))
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    ob = objeto(nombre, me, mat)
    ob.location = pos
    if rot:
        ob.rotation_euler = rot
    return ob


def esfera(nombre, radio, pos=(0, 0, 0), mat=None, escala=(1, 1, 1)):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, radius=radio)
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    ob = objeto(nombre, me, mat)
    ob.location = pos
    ob.scale = escala
    suavizar(ob, 80)
    return ob


def tubo_entre(nombre, p1, p2, radio, mat=None, seg=24):
    p1, p2 = Vector(p1), Vector(p2)
    d = p2 - p1
    ob = cilindro(nombre, radio, d.length, pos=(p1 + p2) / 2, seg=seg, mat=mat)
    ob.rotation_mode = "QUATERNION"
    ob.rotation_quaternion = d.to_track_quat("Z", "Y")
    suavizar(ob, 80)
    return ob


def aplicar(ob):
    """Congela modificadores y transformaciones en la malla."""
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev)
    me.transform(ob.matrix_basis)
    viejo = ob.data
    ob.modifiers.clear()
    ob.data = me
    ob.matrix_basis = Matrix.Identity(4)
    bpy.data.meshes.remove(viejo)
    return ob


def booleana(ob, cortadores, op="DIFFERENCE"):
    for i, c in enumerate(cortadores):
        m = ob.modifiers.new(f"b{i}", "BOOLEAN")
        m.operation = op
        m.object = c
        m.solver = "EXACT"
        c.hide_render = True
        c.hide_viewport = True
    aplicar(ob)
    for c in cortadores:
        bpy.data.objects.remove(c, do_unlink=True)
    suavizar(ob)
    return ob


def unir(objs, nombre):
    base = objs[0]
    booleana(base, objs[1:], "UNION")
    base.name = nombre
    return base


# ---------------------------------------------------------------- piezas
def rejilla(nombre, radio, z, paso, alambre, mat, rayos=6):
    """Rejilla de anillos concéntricos (ranuras de 'paso' mm) con rayos. Se lee como ondas."""
    partes = []
    r = paso + alambre
    while r < radio:
        partes.append(revolucion(f"{nombre}_a", perfil_circulo(r, z, alambre / 2, 8), seg=64, mat=mat))
        r += paso + alambre
    partes.append(revolucion(f"{nombre}_a", perfil_circulo(radio, z, alambre, 8), seg=64, mat=mat))
    for k in range(rayos):
        a = math.pi * k / rayos
        partes.append(caja(f"{nombre}_r", (2 * radio, alambre * 1.2, alambre * 2.2), (0, 0, z), mat, rot=(0, 0, a)))
    return partes


def helice(nombre, diam, z, mat, palas=3):
    partes = [cilindro(f"{nombre}_buje", 0.012, 0.012, (0, 0, z), mat=mat)]
    for k in range(palas):
        a = 2 * math.pi * k / palas
        e = esfera(f"{nombre}_p", 1.0, mat=mat, escala=(diam / 4.1, 0.016, 0.0025))
        e.location = (math.cos(a) * diam / 4, math.sin(a) * diam / 4, z)
        e.rotation_euler = (0.25, 0, a)
        partes.append(e)
    return partes


def motor(nombre, z, mat_carbon, mat_oro, tam=0.017):
    return [cilindro(f"{nombre}_campana", tam, 0.020, (0, 0, z), mat=mat_carbon),
            cilindro(f"{nombre}_eje", 0.004, 0.032, (0, 0, z + 0.008), mat=mat_carbon)]


def cinta_toroide(nombre, R, r, vueltas, ancho, mat, fase=0.0, n=720, despegue=0.0015,
                  rango_v=None):
    """Cinta sobre un toroide (R mayor, r menor). Si rango_v=(A, k) la cinta ondula
    v = A sin(k u) en vez de enroscarse (para cantos donde solo se ve la mitad exterior)."""
    bm = bmesh.new()
    rr = r + despegue
    medio = ancho / 2 / rr
    filas = []
    for i in range(n):
        u = 2 * math.pi * i / n
        if rango_v:
            A, k = rango_v
            v = A * math.sin(k * u + fase)
        else:
            v = vueltas * u + fase
        fila = []
        for dv in (-medio, medio):
            vv = v + dv
            rad = R + rr * math.cos(vv)
            fila.append(bm.verts.new((rad * math.cos(u), rad * math.sin(u), rr * math.sin(vv))))
        filas.append(fila)
    for i in range(n):
        a, b = filas[i], filas[(i + 1) % n]
        bm.faces.new((a[0], b[0], b[1], a[1]))
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    ob = objeto(nombre, me, mat)
    s = ob.modifiers.new("espesor", "SOLIDIFY")
    s.thickness = 0.0015
    s.offset = 1
    aplicar(ob)
    suavizar(ob, 60)
    return ob


# ---------------------------------------------------------------- física
def voxelizar(ob, paso=0.008, dz=0.004):
    """Puntos de volumen interior de una malla cerrada por columnas de rayos verticales."""
    dg = bpy.context.evaluated_depsgraph_get()
    bvh = BVHTree.FromObject(ob, dg)
    bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    xs = [v.x for v in bb]
    ys = [v.y for v in bb]
    zs = [v.z for v in bb]
    z0 = min(zs) - 0.01
    pts = []
    for x in np.arange(min(xs) + paso / 2, max(xs), paso):
        for y in np.arange(min(ys) + paso / 2, max(ys), paso):
            hits = []
            o = Vector((x, y, z0))
            while True:
                loc, nor, idx, dist = bvh.ray_cast(o, Vector((0, 0, 1)))
                if loc is None:
                    break
                hits.append(loc.z)
                o = Vector((x, y, loc.z + 1e-5))
            for a, b in zip(hits[0::2], hits[1::2]):
                for z in np.arange(a + dz / 2, b, dz):
                    pts.append((x, y, z))
    pts = np.array(pts)
    return pts, paso * paso * dz


def area_superficie(ob):
    return sum(p.area for p in ob.data.polygons)


def _rot_x(t):
    c, s = math.cos(t), math.sin(t)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def _hundir(pts, dv, R, peso_total):
    """Altura h tal que el empuje iguala peso_total para la rotación R (bisección)."""
    w = pts @ R.T
    zmin, zmax = w[:, 2].min(), w[:, 2].max()
    lo, hi = -zmax - 0.01, -zmin + 0.01  # h: traslación vertical
    vol_obj = peso_total / (RHO_MAR * G)
    if len(pts) * dv < vol_obj:
        return None, w
    for _ in range(50):
        h = (lo + hi) / 2
        sub = (w[:, 2] + h) < 0
        if sub.sum() * dv > vol_obj:
            lo = h  # sobra volumen hundido: sube
        else:
            hi = h
    return (lo + hi) / 2, w


def equilibrio(pts, dv, masa, cg, carga_n=0.0, punto_carga=(0, 0, 0)):
    """Escora y altura con una carga vertical hacia abajo en punto_carga (eje +y).
    Devuelve el ángulo (positivo = baja el lado +y), la altura y el francobordo del punto."""
    W = masa * G
    cg = np.array(cg)
    pc = np.array(punto_carga)

    def residuo(t):
        R = _rot_x(-t)
        h, w = _hundir(pts, dv, R, W + carga_n)
        if h is None:
            return None, None
        sub = (w[:, 2] + h) < 0
        yb = w[sub, 1].mean()
        B = sub.sum() * dv * RHO_MAR * G
        yg = (R @ cg)[1]
        yl = (R @ pc)[1]
        return B * yb - W * yg - carga_n * yl, h

    ts = np.radians(np.arange(0, 90.5, 1.0))
    prev = None
    for t in ts:
        m, h = residuo(t)
        if m is None:
            return {"hunde": True}
        if prev is not None and np.sign(m) != np.sign(prev[1]):
            a, b = prev[0], t
            for _ in range(30):
                c = (a + b) / 2
                mc, _ = residuo(c)
                if np.sign(mc) == np.sign(prev[1]):
                    a = c
                else:
                    b = c
            t = (a + b) / 2
            _, h = residuo(t)
            R = _rot_x(-t)
            zl = (R @ pc)[2] + h
            return {"escora_deg": round(math.degrees(t), 1), "h": h, "t": t,
                    "francobordo_agarre_mm": round(zl * 1000, 1)}
        prev = (t, m)
    return {"escora_deg": 90.0, "h": None, "t": math.pi / 2, "francobordo_agarre_mm": None,
            "nota": "con esta carga el dron queda parado de canto"}


def curva_carga(pts, dv, masa, cg, punto_carga, paso=2):
    """Carga vertical en el agarre (N) que sostiene cada ángulo de escora entre 0 y 88 grados.
    El máximo de la curva es la carga a partir de la cual el dron se para de canto."""
    W = masa * G
    cg = np.array(cg)
    pc = np.array(punto_carga)
    fmax = len(pts) * dv * RHO_MAR * G - W
    out = []
    for deg in range(0, 89, paso):
        R = _rot_x(-math.radians(deg))

        def res(F):
            h, w = _hundir(pts, dv, R, W + F)
            if h is None:
                return None, None
            sub = (w[:, 2] + h) < 0
            B = sub.sum() * dv * RHO_MAR * G
            return B * w[sub, 1].mean() - W * (R @ cg)[1] - F * (R @ pc)[1], h

        r0, h0 = res(0.0)
        if r0 <= 0:
            out.append((deg, 0.0, h0))
            continue
        lo, hi = 0.0, fmax * 0.999
        rh, hh = res(hi)
        if rh is not None and rh > 0:
            out.append((deg, round(hi, 1), hh))
            continue
        for _ in range(28):
            m = (lo + hi) / 2
            rm, _ = res(m)
            if rm is not None and rm > 0:
                lo = m
            else:
                hi = m
        _, h = res(lo)
        out.append((deg, round(lo, 1), h))
    return out


def pose_con_carga(curva, carga):
    """Primer ángulo donde la curva alcanza la carga. Si nunca la alcanza, se para de canto."""
    prev = None
    for deg, F, h in curva:
        if F >= carga:
            if prev is None:
                return math.radians(deg), h, False
            d0, F0, h0 = prev
            f = (carga - F0) / (F - F0) if F != F0 else 0
            return math.radians(d0 + f * (deg - d0)), h0 + f * (h - h0), False
        prev = (deg, F, h)
    deg, F, h = curva[-1]
    return math.radians(deg), h, True


def curva_adrizamiento(pts, dv, masa, cg, paso=10):
    """GZ (m) entre 0 y 180 grados. Positivo = endereza hacia 0 grados."""
    W = masa * G
    cg = np.array(cg)
    out = []
    for deg in range(0, 181, paso):
        R = _rot_x(-math.radians(deg))
        h, w = _hundir(pts, dv, R, W)
        sub = (w[:, 2] + h) < 0
        yb = w[sub, 1].mean()
        yg = (R @ cg)[1]
        out.append((deg, round((yb - yg) * 1000, 1)))  # mm
    return out


def area_proyectada(pts, paso, cabeceo_deg):
    """Área frontal (m2) con el viento en +x y el dron cabeceado hacia el viento."""
    t = math.radians(cabeceo_deg)
    c, s = math.cos(t), math.sin(t)
    Ry = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    w = pts @ Ry.T
    celdas = set(zip(np.floor(w[:, 1] / paso).astype(int), np.floor(w[:, 2] / paso).astype(int)))
    return len(celdas) * paso * paso


# ---------------------------------------------------------------- render
def preparar_render(res=1400):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x = res
    sc.render.resolution_y = int(res * 0.75)
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    try:
        sc.eevee.taa_render_samples = 64
        sc.eevee.use_shadows = True
    except Exception:
        pass
    w = bpy.data.worlds.new("mundo")
    sc.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes["Background"]
    bg.inputs["Color"].default_value = srgb_to_linear(PALETA["fondo"])
    bg.inputs["Strength"].default_value = 0.55


def luces(cielo=False):
    sol = bpy.data.lights.new("sol", "SUN")
    sol.energy = 2.2 if not cielo else 2.6
    sol.angle = math.radians(8)
    o = objeto("sol", sol)
    o.rotation_euler = (math.radians(38), math.radians(12), math.radians(35))
    area = bpy.data.lights.new("relleno", "AREA")
    area.energy = 120
    area.size = 3
    o2 = objeto("relleno", area)
    o2.location = (-2.5, -2.0, 2.5)
    o2.rotation_euler = Vector((2.5, 2.0, -2.5)).to_track_quat("-Z", "Y").to_euler()


def camara(nombre, objetivo, az, el, dist, lente=70, orto=None):
    cam = bpy.data.cameras.new(nombre)
    cam.lens = lente
    if orto:
        cam.type = "ORTHO"
        cam.ortho_scale = orto
    ob = objeto(nombre, cam)
    a, e = math.radians(az), math.radians(el)
    pos = Vector(objetivo) + dist * Vector((math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)))
    ob.location = pos
    ob.rotation_euler = (Vector(objetivo) - pos).to_track_quat("-Z", "Y").to_euler()
    return ob


def render(cam, ruta):
    sc = bpy.context.scene
    sc.camera = cam
    sc.render.filepath = ruta
    bpy.ops.render.render(write_still=True)


def maniqui(mat, cabeza, mano_izq, mano_der, nombre="persona", codo_alto=-0.04):
    """Persona a escala en el agua: cabeza, cuello, torso vertical y brazos hasta el agarre."""
    cab = Vector(cabeza)
    partes = [esfera(f"{nombre}_cabeza", 0.105, cab, mat, (0.9, 1.0, 1.12))]
    cuello = cab + Vector((0, 0, -0.15))
    hombro_c = cuello + Vector((0, 0, -0.05))
    lado = (Vector(mano_izq) - Vector(mano_der)).normalized()
    hi = hombro_c + lado * 0.20
    hd = hombro_c - lado * 0.20
    partes.append(tubo_entre(f"{nombre}_cuello", cab + Vector((0, 0, -0.06)), cuello, 0.055, mat))
    hom = esfera(f"{nombre}_hombros", 1.0, hombro_c, mat, (0.23, 0.11, 0.075))
    hom.rotation_euler = (0, 0, math.atan2(lado.y, lado.x))
    partes.append(hom)
    partes.append(tubo_entre(f"{nombre}_torso", hombro_c, hombro_c + Vector((0.0, 0.05, -0.65)), 0.16, mat))
    for h, m in ((hi, mano_izq), (hd, mano_der)):
        m = Vector(m)
        codo = (h + m) / 2 + Vector((0, 0, codo_alto))
        partes.append(tubo_entre(f"{nombre}_brazo", h, codo, 0.045, mat))
        partes.append(tubo_entre(f"{nombre}_antebrazo", codo, m, 0.038, mat))
        partes.append(esfera(f"{nombre}_mano", 0.045, m, mat, (1.0, 1.0, 0.7)))
    return partes


# ---------------------------------------------------------------- ficha
def ficha(nombre, P, pts, dv, masa_items, empuje, extra=None, paso=0.008):
    """Calcula la física del concepto y la devuelve como dict.
    pts, dv: vóxeles del volumen estanco que flota.
    masa_items: lista de (nombre, kg, (x, y, z), nota)."""
    vol = len(pts) * dv
    cg_espuma = pts.mean(axis=0)
    masa = sum(m for _, m, _, _ in masa_items)
    cg = sum(np.array(p) * m for _, m, p, _ in masa_items) / masa
    W = masa * G
    reserva = vol * RHO_MAR * G - W

    cc = curva_carga(pts, dv, masa, cg, P["punto_agarre"])
    fpico = max(cc, key=lambda c: c[1])
    persona = {"carga_maxima_antes_de_pararse_n": fpico[1], "a_los_deg": fpico[0],
               "carga_para_escora_n": {f"{d}_deg": F for d, F, _ in cc if d in (10, 20, 30, 45)}}
    for carga in P["cargas_persona_n"]:
        t, h, parado = pose_con_carga(cc, carga)
        persona[f"escora_con_{int(carga)}_n_deg"] = 90.0 if parado else round(math.degrees(t), 1)
        if carga == P["carga_render_n"]:
            if parado:
                t = math.radians(85)
                h, _ = _hundir(pts, dv, _rot_x(-t), W + carga)
            eq = {"t": t, "h": h, "parado": parado}
    # carga máxima en el agarre antes de que se pare de canto (barrido)
    gz = curva_adrizamiento(pts, dv, masa, cg)

    h0, w0 = _hundir(pts, dv, np.eye(3), W)
    calado = (-(w0[:, 2].min() + h0))
    alto = w0[:, 2].max() - w0[:, 2].min()

    a0 = area_proyectada(pts, paso, 0)
    a25 = area_proyectada(pts, paso, 25)
    v = P["viento_rafaga_ms"]
    cd = P["cd"]
    T = empuje["empuje_total_n"]
    # Viento, modelo de placa plana. El dron se inclina t contra la ráfaga. La fuerza normal sobre
    # la cara (N = q Cn A_planta) va sobre el mismo eje que el empuje, así que la paga el empuje.
    # La inclinación la fija el arrastre del canto: W tan(t) = q Cd A_canto. El centro de presión
    # adelantado da un momento de cabeceo que tiene que entrar en la autoridad de los motores.
    # Cn de placa de bajo alargamiento: 2 sen t + 2 sen^2 t con tope 1,1 (aprox., a validar).
    q = 0.5 * RHO_AIRE
    a_planta = area_proyectada(pts, paso, 90)
    cuerda = math.sqrt(4 * a_planta / math.pi)

    # Arrastre de cantidad de movimiento: cada rotor traga aire que llega de costado a la
    # velocidad del viento y lo devuelve vertical. D_ram = m_punto V, con m_punto = sqrt(rho A T / 2)
    # por rotor (teoría de cantidad de movimiento en vuelo estacionario, aprox., a validar).
    # k_giro_ducto: qué fracción de ese aire endereza un ducto poco profundo (aprox., a validar).
    a_rotor = math.pi * (P["helice_pulg"] * 0.0254 / 2) ** 2

    def balance(vv):
        qv = q * vv * vv
        T_req = W
        for _ in range(8):
            ram = P["k_giro_ducto"] * 4 * math.sqrt(RHO_AIRE * a_rotor * T_req / 8) * vv
            t = math.atan((qv * cd * a0 + ram) / W)
            cn = min(1.1, 2 * math.sin(t) + 2 * math.sin(t) ** 2)
            Nn = qv * cn * a_planta
            T_req = Nn + W / math.cos(t)
        momento = Nn * P["cp_excentricidad"] * cuerda
        autoridad = max(T - T_req, 0) * P["brazo_cabeceo_m"]
        balance.ram = ram
        return t, Nn, T_req, momento, autoridad

    t_r, N_r, T_req, mom, aut = balance(v)
    ram_r = balance.ram
    v_max = 0.0
    for vv in np.arange(1.0, 30.0, 0.25):
        t_, _, Tq, mo, au = balance(vv)
        if Tq > T or mo > au or math.degrees(t_) > P["angle_max_deg"]:
            break
        v_max = vv
    # extras: otros puntos de agarre
    for nom, pto in P.get("agarres_extra", {}).items():
        c2 = curva_carga(pts, dv, masa, cg, pto, paso=4)
        persona[f"carga_maxima_agarre_{nom}_n"] = max(F for _, F, _ in c2)

    return {
        "concepto": nombre,
        "parametros": dict(P),
        "volumen_estanco_l": round(vol * 1000, 2),
        "masa_kg": round(masa, 3),
        "cg_mm": [round(c * 1000, 1) for c in cg],
        "cb_espuma_mm": [round(c * 1000, 1) for c in cg_espuma],
        "masa_detalle": [{"pieza": n, "kg": round(m, 3), "nota": nt} for n, m, _, nt in masa_items],
        "flotacion_total_n": round(vol * RHO_MAR * G, 1),
        "reserva_flotacion_n": round(reserva, 1),
        "calado_mm": round(calado * 1000, 1),
        "francobordo_mm": round((alto - calado) * 1000, 1),
        "persona_agarrada": persona,
        "_pose": {"h": eq.get("h"), "t": eq.get("t")},
        "gz_mm": gz,
        "area_frontal_m2": {"cabeceo_0": round(a0, 4), "cabeceo_25": round(a25, 4)},
        "viento": {"rafaga_ms": v, "cd_canto": cd, "area_planta_m2": round(a_planta, 4),
                   "area_canto_m2": round(a0, 4),
                   "inclinacion_deg": round(math.degrees(t_r), 1),
                   "fuerza_normal_cara_n": round(N_r, 1),
                   "arrastre_rotores_n": round(ram_r, 1),
                   "empuje_necesario_n": round(T_req, 1),
                   "empuje_disponible_n": round(T, 1),
                   "momento_cabeceo_nm": round(mom, 2),
                   "autoridad_cabeceo_nm": round(aut, 2),
                   "viento_max_sostenible_ms": round(v_max, 2),
                   "nota": "placa plana con Cn y centro de presión aprox., a validar en túnel o en vuelo"},
        "empuje": empuje,
        "relacion_empuje_peso": round(T / W, 2),
        **(extra or {}),
    }


def empuje_motores(n, kg_por_motor, k_ducto, k_rejilla):
    t = n * kg_por_motor * k_ducto * k_rejilla * G
    return {"motores": n, "kg_por_motor_libre": kg_por_motor, "k_ducto": k_ducto,
            "k_rejilla": k_rejilla, "empuje_total_n": round(t, 1),
            "nota": "empuje por motor, ganancia del ducto y pérdida de rejilla: aprox., a validar en banco"}


def guardar(nombre, datos, carpeta):
    os.makedirs(carpeta, exist_ok=True)
    with open(os.path.join(carpeta, f"{nombre}_ficha.json"), "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def masa_comun(P, vol_espuma_l, area_piel_m2, ductos, cg_espuma=(0, 0, 0)):
    """Presupuesto de masa compartido. Todo aprox., a validar con pesadas reales."""
    zb = P.get("z_bateria", -0.01)
    it = [
        ("espuma EPP", vol_espuma_l * P["densidad_espuma_kg_l"], tuple(cg_espuma), "EPP de celda cerrada, unos 30 g/L (aprox., a validar)"),
        ("piel y pintura", area_piel_m2 * P["piel_kg_m2"], tuple(cg_espuma), "recubrimiento elástico sobre la espuma (aprox., a validar)"),
        ("batería LiPo 6S 3000 mAh", P.get("masa_bateria_kg", 0.48), P.get("pos_bateria", (0, 0, zb)), "vuelo de pocos minutos, en el agua solo queda la baliza. LiPo de FPV para dar la corriente de pico (aprox., a validar)"),
        ("caja estanca central", 0.18, P.get("pos_caja", (0, 0, 0)), "PETG con tapa y o-ring (aprox., a validar)"),
        ("controladora, ESC, GPS, radios", 0.10, P.get("pos_caja", (0, 0, 0.02)), "aprox., a validar"),
        ("computadora y cámara a bordo (D-021)", 0.06, P.get("pos_caja", (0, 0, -0.02)), "aprox., a validar"),
        ("baliza, buzzer, sensor de agua, cableado", 0.08, (0, 0, 0.0), "aprox., a validar"),
        ("estructura de carbono", P["masa_frame_kg"], (0, 0, 0), "brazos o aro de carbono embebidos (aprox., a validar)"),
    ]
    for i, (x, y) in enumerate(ductos):
        it.append((f"motor {i + 1}", P["masa_motor_kg"], (x, y, 0.0), "motor brushless para agua de mar (aprox., a validar)"))
        it.append((f"hélice {i + 1}", P["masa_helice_kg"], (x, y, 0.012), "aprox., a validar"))
        it.append((f"rejillas ducto {i + 1}", 2 * P["masa_rejilla_kg"], (x, y, 0.0), "arriba y abajo (aprox., a validar)"))
    return it


def correr(nombre, P, construir, extra=None, materiales=None):
    """Arma el concepto, calcula la ficha, renderiza estudio y agua y guarda .blend."""
    limpiar()
    preparar_render(P.get("res", 1400))
    M = (materiales or mats)()
    g = construir(P, M)
    cuerpo = g["cuerpo"]
    pts, dv = voxelizar(cuerpo, P.get("paso_voxel", 0.008))
    vol_l = len(pts) * dv * 1000
    vol_espuma = vol_l - g.get("vol_no_espuma_l", 1.3)
    area_piel = area_superficie(cuerpo) - g.get("area_sin_piel_m2", 0.0)
    items = masa_comun(P, vol_espuma, area_piel, g["ductos"], tuple(pts.mean(axis=0)))
    items += g.get("masa_extra", [])
    emp = empuje_motores(4, P["kg_por_motor"], P["k_ducto"], P["k_rejilla"])
    P.setdefault("brazo_cabeceo_m", float(np.mean([abs(x) for x, _ in g["ductos"]])))
    datos = ficha(nombre, P, pts, dv, items, emp, extra)
    datos["rejilla"] = {"abertura_mm": P["abertura_rejilla"] * 1000,
                        "distancia_helice_mm": round(g.get("dist_rejilla", 0) * 1000, 1),
                        "iso_13857": "ranura de 4 a 6 mm pide 10 mm de distancia (tabla 4, 14 años o más)"}
    datos["dimensiones_mm"] = {"diametro_o_largo": round(g["envergadura"] * 1000), "alto": round(g["alto"] * 1000)}

    raiz = bpy.data.objects.new("gavia", None)
    bpy.context.scene.collection.objects.link(raiz)
    for ob in bpy.context.scene.objects:
        if ob is not raiz and ob.type == "MESH" and ob.parent is None:
            ob.parent = raiz

    carpeta = os.path.join(HERE, "renders", nombre)
    os.makedirs(carpeta, exist_ok=True)
    luces()
    piso = cilindro("piso", 40, 0.01, (0, 0, -0.32), mat=M["fondo"])
    span = g["envergadura"]
    d = span * 3.0
    render(camara("c34", (0, 0, 0), -55, 28, d), os.path.join(carpeta, "1_tres_cuartos.png"))
    render(camara("cfr", (0, 0, 0), -90, 4, d), os.path.join(carpeta, "2_frente.png"))
    render(camara("cdet", (0, span * 0.25, 0.02), -30, 22, d * 0.45), os.path.join(carpeta, "4_detalle.png"))
    # arriba y abajo sin piso, para que el hueco se lea como hueco
    piso.hide_render = True
    render(camara("cup", (0, 0, 0), -90, 89.9, d, orto=span * 1.35), os.path.join(carpeta, "3_arriba.png"))
    if P.get("render_abajo"):
        render(camara("cdn", (0, 0, 0), -90, -89.9, d, orto=span * 1.35), os.path.join(carpeta, "7_abajo.png"))

    # en el agua, con un adulto agarrado del lado +y, en la pose de equilibrio calculada
    bpy.data.objects.remove(piso, do_unlink=True)
    pose = datos["_pose"]
    if pose.get("h") is not None:
        t, h = pose["t"], pose["h"]
        raiz.rotation_euler = (-t, 0, 0)
        raiz.location = (0, 0, h)
        bpy.context.view_layer.update()
        Rw = raiz.matrix_world
        mi = Rw @ Vector(g["manos"][0])
        md = Rw @ Vector(g["manos"][1])
        y_c = max(mi.y, md.y) + 0.24
        maniqui(M["piel"], (0, y_c, 0.16), mi, md, codo_alto=g.get("codo_alto", -0.04))
        agua = cilindro("agua", 8, 0.002, (0, 0, -0.001), seg=8, mat=M["agua"])
        if g.get("baliza") is not None and "baliza_on" in M:
            g["baliza"].data.materials.clear()
            g["baliza"].data.materials.append(M["baliza_on"])
        render(camara("cagua", (0, 0.25, 0.0), -35, 20, d * 1.1), os.path.join(carpeta, "5_agua.png"))
        render(camara("cagua2", (0, 0.2, 0.0), 160, 14, d * 1.0), os.path.join(carpeta, "6_agua_guardavidas.png"))

    datos.pop("_pose", None)
    guardar(nombre, datos, carpeta)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, f"{nombre}.blend"))
    print("FICHA", json.dumps({k: datos[k] for k in ("volumen_estanco_l", "masa_kg", "reserva_flotacion_n",
                                                     "relacion_empuje_peso", "persona_agarrada", "viento")},
                              ensure_ascii=False))
    return datos


# parámetros compartidos por los tres conceptos (aprox., a validar)
BASE = {
    "densidad_espuma_kg_l": 0.030,
    "piel_kg_m2": 0.30,
    "masa_motor_kg": 0.055,
    "masa_helice_kg": 0.012,
    "masa_rejilla_kg": 0.030,
    "masa_frame_kg": 0.15,
    "k_ducto": 1.10,  # la teoría de cantidad de movimiento da hasta 1,26 con ducto ideal
    "k_rejilla": 0.85,
    "abertura_rejilla": 0.006,
    "alambre_rejilla": 0.0018,
    # adulto agarrado de un lado: 40 N es el mínimo para un adulto consciente (Restube) y
    # 100 N el piso de un rescue tube (RLSSA SE12). El render muestra la pose con 40 N.
    "cargas_persona_n": (40.0, 100.0),
    "carga_render_n": 40.0,
    "viento_rafaga_ms": 14.0,  # ráfagas de unos 50 km/h en días sin alerta en Mar del Plata (prensa local)
    "cd": 1.1,
    "angle_max_deg": 45.0,  # ArduCopter permite subir ANGLE_MAX (por defecto 30) hasta 80
    "k_giro_ducto": 0.6,  # ducto de 90 mm para hélice de 203 mm: endereza el flujo solo en parte
    "cp_excentricidad": 0.12,  # centro de presión adelantado, fracción de la cuerda (aprox., a validar)
}


# ---------------------------------------------------------------- ronda de refinamiento
def rejilla_fleje(nombre, radio, z, paso, espesor, prof, mat, angulo=0.0, aro_ancho=0.004, nervios=0):
    """Rejilla de flejes paralelos (barras planas de 'espesor' y 'prof' de alto, alineadas con
    el flujo), con un aro estructural. Ranura libre = paso. Distinta de la rejilla de anillos y
    rayos del TY-3R y más simple de fabricar (aprox., a validar en banco)."""
    partes = []
    p = paso + espesor
    n = int(radio / p)
    for i in range(-n, n + 1):
        y = i * p
        if abs(y) >= radio - espesor:
            continue
        largo = 2 * math.sqrt(radio * radio - y * y)
        b = caja(f"{nombre}_f", (largo, espesor, prof), (0, 0, z), mat)
        b.location = (-y * math.sin(angulo), y * math.cos(angulo), z)
        b.rotation_euler = (0, 0, angulo)
        partes.append(b)
    for k in range(nervios):
        x = -radio + 2 * radio * (k + 1) / (nervios + 1)
        largo = 2 * math.sqrt(radio * radio - x * x)
        b = caja(f"{nombre}_n", (espesor * 1.3, largo, prof), mat=mat)
        b.location = (x * math.cos(angulo), x * math.sin(angulo), z)
        b.rotation_euler = (0, 0, angulo)
        partes.append(b)
    partes.append(revolucion(f"{nombre}_aro",
                             perfil_estadio(radio - aro_ancho / 2, radio + aro_ancho / 2, prof, radio=0.0008),
                             seg=96, mat=mat))
    for pt in partes[-1:]:
        pt.location.z = z
    return partes


def _arco_perfil(perfil):
    pts = np.array(perfil + [perfil[0]])
    seg = np.sqrt(((pts[1:] - pts[:-1]) ** 2).sum(axis=1))
    return pts, np.concatenate([[0], np.cumsum(seg)])


def _punto_perfil(pts, acum, s):
    L = acum[-1]
    s = s % L
    i = int(np.searchsorted(acum, s, side="right") - 1)
    i = min(i, len(pts) - 2)
    f = (s - acum[i]) / max(acum[i + 1] - acum[i], 1e-9)
    p = pts[i] + f * (pts[i + 1] - pts[i])
    d = pts[i + 1] - pts[i]
    nrm = np.array([d[1], -d[0]]) / max(np.hypot(*d), 1e-9)
    return p, nrm


def cinta_perfil(nombre, perfil, vueltas, ancho, mat, s0=0.0, despegue=0.0004, n=900, s_cara=None, acel=0.0):
    """Faja sobre un sólido de revolución de perfil cerrado: avanza 'vueltas' veces el contorno
    de la sección mientras da una vuelta al aro. Con vueltas=1 envuelve la sección una sola vez.
    acel > 0 hace que cruce las caras (centradas en s_cara) más rápido y se demore en las paredes."""
    pts, acum = _arco_perfil(perfil)
    L = acum[-1]
    # sentido de las normales: hacia afuera del perfil
    cen = pts[:-1].mean(axis=0)
    p0, n0 = _punto_perfil(pts, acum, 0.0)
    signo = 1.0 if np.dot(p0 - cen, n0) > 0 else -1.0
    bm = bmesh.new()
    filas = []
    k = 9  # puntos a lo ancho, cada uno apoyado sobre el perfil para que la faja copie los cantos
    for i in range(n):
        u = 2 * math.pi * i / n
        s = s0 + vueltas * L * i / n
        if acel and s_cara is not None:
            psi = (s - s_cara) / L
            s = s + acel * L * math.sin(4 * math.pi * psi) / (4 * math.pi)
        fila = []
        for j in range(k):
            ds = -ancho / 2 + ancho * j / (k - 1)
            p, nr = _punto_perfil(pts, acum, s + ds)
            r, z = p + signo * nr * despegue
            fila.append(bm.verts.new((r * math.cos(u), r * math.sin(u), z)))
        filas.append(fila)
    for i in range(n):
        a, b = filas[i], filas[(i + 1) % n]
        for j in range(k - 1):
            bm.faces.new((a[j], b[j], b[j + 1], a[j + 1]))
    me = bpy.data.meshes.new(nombre)
    bm.to_mesh(me)
    bm.free()
    ob = objeto(nombre, me, mat)
    sol = ob.modifiers.new("espesor", "SOLIDIFY")
    sol.thickness = 0.001
    sol.offset = 0
    aplicar(ob)
    suavizar(ob, 60)
    return ob


def mats_r1():
    """Paleta corregida por los críticos: cuerpo mate, oro satinado en el tono profundo,
    rejillas en gris cálido, naranja solo donde hay hélice."""
    M = mats()
    M["cuerpo"] = material("cuerpo_mate", "crema", rough=0.62)
    M["oro"] = material("oro_satinado", "oro_profundo", rough=0.35, metal=0.35)
    M["rejilla"] = material("rejilla", "naranja", rough=0.55)
    M["ducto"] = material("ducto_naranja", "naranja", rough=0.55)
    M["linea"] = material("linea", "linea", rough=0.6)
    M["baliza_lente"] = material("baliza_lente", "#4A4642", rough=0.15)
    M["baliza_on"] = material("baliza_on", "naranja", rough=0.2, emit=1.6)
    return M
